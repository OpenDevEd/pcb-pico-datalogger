Sensors
=======

AHT20
-----

  - Measures temperature and humidity.
  - Status: implemented
  - I2C-Breakout: (Adafruit  4566)[https://adafru.it/4566]
  - Address: 0x38
  - Guide: <https://learn.adafruit.com/adafruit-aht20>
  - CircuitPython-driver: <https://github.com/adafruit/Adafruit_CircuitPython_AHTx0>
  - [datasheet](https://cdn-learn.adafruit.com/assets/assets/000/091/676/original/AHT20-datasheet-2020-4-16.pdf?1591047915)


AM2301B
-------

  - Measures temperature and humidity (is an AHT20 in an enclosure)
  - Status: implemented
  - I2C-Breakout: (Adafruit  5181)[https://adafru.it/5181]
  - Address: 0x38
  - Guide: <https://learn.adafruit.com/adafruit-aht20>
  - CircuitPython-driver: <https://github.com/adafruit/Adafruit_CircuitPython_AHTx0>
  - [datasheet](https://cdn-shop.adafruit.com/product-files/5181/5181_AM2301B.pdf)
  - Note: non-standard wiring:  
    Red: 3V3, Black: GND, White: SCL, Yellow: SDA


SHT45
-----

  - Measures temperature and humidity
  - Status: planned
  - I2C-Breakout: (Adafruit  ????)[https://adafru.it/????]
  - Address: 
  - Guide: https://sensirion.com/products/catalog/SHT45/
  - CircuitPython-driver:
  - [datasheet]()


MCP9808
-------

  - Measures temperature
  - Status: implemented
  - I2C-Breakout: (Adafruit  ????)[https://adafru.it/????]
  - Address: 
  - Guide: 
  - CircuitPython-driver:
  - [datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/25095A.pdf)


BH1745
------

  - Measures 
  - Status: planned
  - I2C-Breakout: (Adafruit  ????)[https://adafru.it/????]
  - Address: 
  - Guide: 
  - CircuitPython-driver:
  - [datasheet]()


LTR-559
-------

  - Measures 
  - Status: implemented
  - I2C-Breakout: (Adafruit  ????)[https://adafru.it/????]
  - Address: 
  - Guide: 
  - CircuitPython-driver:
  - [datasheet]()


PDM-Micro
---------

  - Measures 
  - Status: implemented
  - I2C-Breakout: (Adafruit  ????)[https://adafru.it/????]
  - Address: 
  - Guide: 
  - CircuitPython-driver:
  - [datasheet]()


Please note that many of the Adafruit versions of the above sensors are fitted with an LED. For some sensors, this can be disabled by cutting a track, but for others there is no straightforward way of diabling the LED.


Microcontroller
===============


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
- Micro-SD Card Reader/connector/socket: <https://datasheet.lcsc.com/lcsc/1912111437_SHOU-HAN-TF-PUSH_C393941.pdf>
- Oscillator: <https://datasheet.lcsc.com/lcsc/1810171817_Seiko-Epson-Q13FC1350000400_C32346.pdf>
- CR2032-Holder: <https://datasheet.lcsc.com/lcsc/2012121836_MYOUNG-BS-08-B2AA001_C964777.pdf>

