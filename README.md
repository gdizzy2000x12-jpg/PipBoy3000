# Pip-Boy 3000 Mark IV — Personal Build

Field documentation for a wearable Pip-Boy 3000 based on
[robegamesios/PipBoy3000](https://github.com/robegamesios/PipBoy3000).

Firmware and STL files stay with the upstream repository. This repo holds the
build binder used on the bench.

## Documents

| File | What it is |
| --- | --- |
| `docs/PipBoy3000_Wasteland_Survival_Guide.pdf` | Combined Fallout-themed manual: salvage list, plates, wiring, staged tests |
| `docs/PipBoy3000_Instruction_Manual.pdf` | Illustrated electronics manual |
| `docs/PipBoy3000_Parts_Checklist.html` | Interactive parts checklist (open in a browser) |
| `docs/PipBoy3000_Board_Assembly_and_Test_Guide.html` | Bench assembly and test procedure |

## Upload docs from your computer

Place the PDF and HTML files in the same folder as `scripts/upload_to_github.py`, then:

```bash
export GITHUB_TOKEN=ghp_your_token_here
python3 scripts/upload_to_github.py
```

Optional overrides:

```bash
python3 scripts/upload_to_github.py --owner gdizzy2000x12-jpg --repo PipBoy3000 --branch main
```

The token needs permission to write repository contents.

## Bench rule

Do not mount the electronics in the printed housing until every test in the
Survival Guide Chapter V / decision gate has passed.
