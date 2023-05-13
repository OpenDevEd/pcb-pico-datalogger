Links
=====

This is a collection of links to products, datasheets, documentation and so on.

Datasheets for hardware used in conjunction with the board
----------------------------------------------------------

- Raspberry Pi Pico or Pico W (https://www.raspberrypi.com/products/raspberry-pi-pico/) or a pin-compatible device, such as the [Pico Lipo](https://shop.pimoroni.com/products/pimoroni-pico-lipo) is required for the operation of the board. Details on which device to chose are below.
- Adafruit RFM96W LoRa Radio Transceiver Breakout - 433 MHz - RadioFruit:  
  <https://www.adafruit.com/product/3073>
  This is optional. It is used for offloading data from the Pico to a 'base station'. If you have public LoRa gateways where you are, you can also use one of those gateways.
  *Important:* We are selecting the 433 MHz version of this board, as this is the appropriate frequency for Tanzania. There is an 868 / 915 MHz version available https://www.adafruit.com/product/3072.
- Pico Inky Pack:  
  <https://shop.pimoroni.com/products/pico-inky-pack>
  Optional. Used to shows sensor data.
  This is optional.

The board is intended to be used with I2C sensors. We have not finalised the selection of sensors, but are trialling:
- AHT20 (temperature and humidity), [Adafruit with Qw/ST](https://www.adafruit.com/product/4566), [data sheet](https://cdn-learn.adafruit.com/assets/assets/000/091/676/original/AHT20-datasheet-2020-4-16.pdf?1591047915), I2C address 0x38
- Asair AM2301B in enclosure [datasheet](https://cdn-shop.adafruit.com/product-files/5181/5181_AM2301B.pdf), I2C address 0x38
- SHT45 (temperature and humidity), https://sensirion.com/products/catalog/SHT45/
- MCP9808 (temperature), https://ww1.microchip.com/downloads/en/DeviceDoc/25095A.pdf
- BH1745 (light)
- LTR-559 (light)
- MEMS Microphone (details to follow)

Please note that many of the Adafruit versions of the above sensors are fitted with an LED. For some sensors, this can be disabled by cutting a track, but for others there is no straightforward way of diabling the LED.

Picking the right micro controller for connectivity and storage
----

How will you store data? The Pico has only provided 848 kB with MicroPython installed, much of which will be taken up by software. If you do not 'offload data' (or want your data to be storage on the device), you need more storage.
- If 'offload data' via LoRa, and do not need storage on the device, use any of the above (Pico, Pico W, Pico Lipo)
- If you do need storage on the device, you can use either:
  - Any of the above devices together with a mico-SD card, inserted into the micro-SD card slot of our device. This has the disadvantage that the micr-SD card is an extra expense. However, the advantage is that you get a large amount of storage.
  - If you measure infrequently (e.g., a few times an hour), then your storage needs may only be a few MB. If you do not want to use an SD card, and you do not need WiFi, you can use the Pico Lipo (4 MB or 16 MB).

Do you need WiFi? WiFi could be useful if you want to use the device in a setting where there is a WiFi network readily available. WiFi could also be useful for accessing the device for inspection (similarly to configuring an https://shop.pimoroni.com/products/enviro-indoor). 
- If you need WiFi (instead of LoRa or in addition to LoRa), use the Pico W.
- Otherwise use the Raspberry Pi Pico or the Pimoroni Pico Lipo.


Power
-----
The board needs to be powered with one of the following options:
- Two AA or AAA batteries
- AA or AAA rechargeables (take care to get the 'slow discharge' type)
- A LiPo battery

The RTC requires a CR2032 cell. The RTC is powered separately, so that the batteries can be changed without losing time.


Datasheets for components used on the board
-------------------------------------------

Note: some of the components can be replaced with similar components but this might
need some rework on the pcb.

- PCF8523: <https://www.nxp.com/docs/en/data-sheet/PCF8523.pdf>
- SN74HC74: <https://www.ti.com/lit/ds/symlink/sn74hc74.pdf>
- Micro-SD Card Reader: <https://datasheet.lcsc.com/lcsc/1912111437_SHOU-HAN-TF-PUSH_C393941.pdf>
- Oscillator: <https://datasheet.lcsc.com/lcsc/1810171817_Seiko-Epson-Q13FC1350000400_C32346.pdf>
- CR2032-Holder: <https://datasheet.lcsc.com/lcsc/2012121836_MYOUNG-BS-08-B2AA001_C964777.pdf>


Software
--------

To follow.

Background
----------
For background on / motivation for this project, please see https://opendeved.net/programmes/ilce-in-tanzania/.
