#!/usr/bin/env python3
"""
Upload Pip-Boy 3000 field docs to a GitHub repository.

Usage:
  export GITHUB_TOKEN=ghp_your_token_here
  python3 upload_to_github.py

Optional:
  python3 upload_to_github.py --owner YOUR_USER --repo PipBoy3000 --branch main

The token needs the "repo" scope (classic) or Contents: Read and write (fine-grained).
Create a token at https://github.com/settings/tokens
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_OWNER = "gdizzy2000x12-jpg"
DEFAULT_REPO = "PipBoy3000"
DEFAULT_BRANCH = "main"
API = "https://api.github.com"

SCRIPT_DIR = Path(__file__).resolve().parent
SEARCH_DIRS = [
    Path.cwd(),
    SCRIPT_DIR,
    SCRIPT_DIR.parent,
    SCRIPT_DIR.parent / "docs",
    Path("/home/workdir/artifacts"),
]

UPLOAD_MAP = [
    ("PipBoy3000_Wasteland_Survival_Guide.pdf", "docs/PipBoy3000_Wasteland_Survival_Guide.pdf"),
    ("PipBoy3000_Instruction_Manual.pdf", "docs/PipBoy3000_Instruction_Manual.pdf"),
    ("PipBoy3000_Parts_Checklist.html", "docs/PipBoy3000_Parts_Checklist.html"),
    ("PipBoy3000_Board_Assembly_and_Test_Guide.html", "docs/PipBoy3000_Board_Assembly_and_Test_Guide.html"),
    ("upload_to_github.py", "scripts/upload_to_github.py"),
]


def find_local(name: str) -> Path | None:
    if name == "upload_to_github.py":
        return Path(__file__).resolve()
    for folder in SEARCH_DIRS:
        candidate = folder / name
        if candidate.is_file():
            return candidate
    return None


def api(token: str, method: str, url: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GitHub API {exc.code} {url}\n{body}") from exc


def get_sha(token: str, owner: str, repo: str, path: str, branch: str) -> str | None:
    url = f"{API}/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    try:
        info = api(token, "GET", url)
    except SystemExit as exc:
        if "404" in str(exc):
            return None
        raise
    return info.get("sha")


def put_file(token: str, owner: str, repo: str, branch: str, dest: str, source: Path) -> None:
    content_b64 = base64.b64encode(source.read_bytes()).decode("ascii")
    sha = get_sha(token, owner, repo, dest, branch)
    payload = {
        "message": f"Add or update {dest}",
        "content": content_b64,
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha
        payload["message"] = f"Update {dest}"
    url = f"{API}/repos/{owner}/{repo}/contents/{dest}"
    result = api(token, "PUT", url, payload)
    html = result.get("content", {}).get("html_url", dest)
    print(f"uploaded: {html}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload Pip-Boy 3000 docs to GitHub")
    parser.add_argument("--owner", default=os.environ.get("GITHUB_OWNER", DEFAULT_OWNER))
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPO", DEFAULT_REPO))
    parser.add_argument("--branch", default=os.environ.get("GITHUB_BRANCH", DEFAULT_BRANCH))
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"))
    args = parser.parse_args()

    if not args.token:
        print("Set GITHUB_TOKEN (or pass --token).", file=sys.stderr)
        print("https://github.com/settings/tokens", file=sys.stderr)
        return 2

    print(f"Target: https://github.com/{args.owner}/{args.repo}  branch={args.branch}")
    for name, dest in UPLOAD_MAP:
        source = find_local(name)
        if source is None:
            print(f"skip (missing): {name}")
            continue
        put_file(args.token, args.owner, args.repo, args.branch, dest, source)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
