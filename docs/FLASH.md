# Flash the firmware to the ESP32

Images are compiled into the sketch as C headers. You do **not** upload a SPIFFS image. MP3 files go on the DFPlayer microSD card.

## 1. Arduino IDE and ESP32 core

1. Install Arduino IDE 2.x.
2. File → Preferences → Additional boards manager URLs:
   `https://espressif.github.io/arduino-esp32/package_esp32_index.json`
3. Tools → Board → Boards Manager → install **esp32** by Espressif. Prefer 2.0.x if 3.x breaks ESP8266Audio.
4. If Windows does not show a COM port, install the CP2102 or CH340 driver that matches the chip next to the USB socket.

## 2. Libraries (Library Manager)

| Library | Notes |
| --- | --- |
| TFT_eSPI (Bodmer) | Must edit User_Setup.h after install |
| WiFiManager (tzapu) | Included by the sketch |
| NTPClient (Fabrice Weinberg) | Clock |
| DFRobotDFPlayerMini | SD audio |
| Adafruit AHTX0 | Pulls in Adafruit BusIO |
| AnimatedGIF (bitbank2) | Boot and menu GIFs |
| ESP8266Audio (earlephilhower) | Internet radio (`AudioFileSourceICYStream`, `AudioOutputI2S`) |

If ESP8266Audio is missing from Library Manager, clone it into `Documents/Arduino/libraries/`.

Keep these three together in one folder or compile will fail:

- `Fallout_PipBoy3000_Fahrenheit.ino`
- `GIFDraw.ino`
- `images/`

## 3. TFT_eSPI pins (do this before any compile)

Copy `docs/PipBoy3000_User_Setup.h` over `Documents/Arduino/libraries/TFT_eSPI/User_Setup.h`.

Default pins in that file (VSPI, so GPIO 12/13/14 stay free for the PCM5102A):

- MOSI 23, SCLK 18, MISO 19, CS 5, DC 2, RST 4
- Driver: `ILI9488_DRIVER` unless the panel silkscreen says otherwise
- Size: 320 × 480

A TFT_eSPI update overwrites this file. Keep a spare copy.

## 4. Credentials in the sketch

```cpp
const char *ssid = "YOUR_2.4GHZ_SSID";
const char *password = "YOUR_WIFI_PASSWORD";
int UTC = -5;                       // 3600 * UTC seconds; Central daylight example
uint16_t notification_volume = 25;  // 0–30
#define DEBUG 1
```

Classic ESP32-WROOM is 2.4 GHz only.

## 5. Tools menu

| Setting | Value |
| --- | --- |
| Board | ESP32 Dev Module |
| Upload Speed | 115200 if 921600 fails |
| CPU Frequency | 240 MHz |
| Flash Frequency | 80 MHz |
| Flash Mode | QIO |
| Flash Size | 4 MB (unless marked otherwise) |
| Partition Scheme | **Minimal SPIFFS (1.9 MB APP with OTA / 190 KB SPIFFS)** or Huge APP |
| PSRAM | Disabled unless the board has PSRAM |
| Port | This board’s COM / tty / cu.usbserial port |

Default partitions often fail because the GIF headers make the sketch large.

## 6. Compile, then upload

1. Sketch → Verify/Compile. Fix errors before upload.
2. Close Serial Monitor so it does not lock the port.
3. Sketch → Upload.
4. If the log sticks on `Connecting........`:
   - hold **BOOT** (IO0)
   - tap **EN** / RESET
   - release BOOT after `Writing at` starts
5. Success looks like `Hash of data verified` then `Hard resetting via RTS pin`.

Charge-only cables never leave Connecting.

## 7. First boot

Serial Monitor at **115200**. Press EN.

Expected: Wi-Fi, then DFPlayer online or an SD error, then AHT init, then the INIT animation.

The sketch **halts in setup()** if DFPlayer or AHT20 is missing. That means the flash worked and the firmware is waiting on wiring.

MP3s are not part of the flash. FAT32 card, folder `mp3`, files `0001.mp3` …

## Compile faults

| Message | Fix |
| --- | --- |
| GIFDraw not declared | `GIFDraw.ino` not in the sketch folder |
| images/INIT.h missing | `images/` folder not copied |
| AudioFileSourceICYStream.h | Install ESP8266Audio |
| sketch too big / iram overflow | Change Partition Scheme |
| TFT pins undefined | Restore `PipBoy3000_User_Setup.h` |
