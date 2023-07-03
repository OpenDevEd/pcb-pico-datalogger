Pins
====


Reserved Pins on Raspberry Pi Pico
----------------------------------

Note that the default I2C-bus is I2C1. The UART-header could also
be used for I2C0.

If LoRa is not used, the LoRa pins GP8/GP9 also provide I2C0.


|                     | Pin  | Pin  |                         |
|---------------------|------|------|-------------------------|
| UART-TX / I2C0-SDA  | GP0  | VBUS |
| UART-RX / I2C0-SCL  | GP1  | VSYS |
|                     | GND  | GND  |
| I2C1-SDA (RTC)      | GP2  | EN   |
| I2C1-SCL (RTC)      | GP3  | 3V3  |
| DONE                | GP4  | VREF |
| I2S/PDM (BCLK/CLK)  | GP5  | GP28 | I2S/PDM (DOUT/DAT)
|                     | GND  | GND  |
| I2S (LRCL)          | GP6  | GP27 | ADC ext
| LoRa-RST            | GP7  | GP26 | Inky Busy
| MISO1 (LoRa)        | GP8  | RUN  | Inky Run
| LoRa-CS             | GP9  | GP22 | SD-CS
|                     | GND  | GND  |
| SCLK1 (LoRa)        | GP10 | GP21 | Inky Reset
| MOSI1 (LoRa)        | GP11 | GP20 | Inky D/C
| Inky SWA            | GP12 | GP19 | MOSI0 (Inky, SD-Card)
| Inky SWB            | GP13 | GP18 | SCLK0 (Inky, SD-Card)
|                     | GND  | GND  |
| Inky SWC            | GP14 | GP17 | Inky CS
| LoRa-EN             | GP15 | GP16 | MISO0 (Inky, SD-Card)
