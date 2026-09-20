// Pip-Boy 3000 — TFT_eSPI User_Setup.h
// Copy this over Arduino/libraries/TFT_eSPI/User_Setup.h
// OR include it from User_Setup_Select.h instead of the default.
//
// Pins below use ESP32 VSPI so GPIO 12/13/14 stay free for the PCM5102A.
// Change ONLY the DRIVER and WIDTH/HEIGHT lines if your panel is different.

#define USER_SETUP_INFO "PipBoy3000"

// Uncomment ONE driver that matches the chip printed on the back of the TFT.
#define ILI9488_DRIVER
//#define ST7796_DRIVER
//#define ILI9341_DRIVER
//#define ILI9486_DRIVER

#define TFT_WIDTH  320
#define TFT_HEIGHT 480

// VSPI — do not use 12, 13, or 14 (I2S radio DAC).
#define TFT_MISO 19
#define TFT_MOSI 23
#define TFT_SCLK 18
#define TFT_CS    5
#define TFT_DC    2
#define TFT_RST   4

// Backlight is usually tied to 3.3 V or 5 V on the panel, not a GPIO.
//#define TFT_BL   32
//#define TFT_BACKLIGHT_ON HIGH

#define LOAD_GLCD
#define LOAD_FONT2
#define LOAD_FONT4
#define LOAD_FONT6
#define LOAD_FONT7
#define LOAD_FONT8
#define LOAD_GFXFF
#define SMOOTH_FONT

#define SPI_FREQUENCY        27000000
#define SPI_READ_FREQUENCY   20000000
#define SPI_TOUCH_FREQUENCY   2500000
