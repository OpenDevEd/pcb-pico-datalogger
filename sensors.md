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


BH1750
------

  - Measures Light
  - Status: implemented
  - I2C-Breakout: (Adafruit  4681)[https://adafru.it/4681]
  - Address: 0x23 (default) or 0x5C (addr-pin high)
  - Guide: <https://learn.adafruit.com/adafruit-bh1750-ambient-light-sensor>
  - CircuitPython-driver: <https://github.com/adafruit/Adafruit_CircuitPython_BH1750>
  - [datasheet](https://www.mouser.com/datasheet/2/348/bh1750fvi-e-186247.pdf)


LTR-559
-------

  - Measures Light
  - Status: implemented
  - I2C-Breakout: (Pimoroni PIM413)[https://shop.pimoroni.com/products/ltr-559-light-proximity-sensor-breakout)]
  - Address: 0x23
  - Guide: n.a.
  - CircuitPython-driver: <https://github.com/pimoroni/Pimoroni_CircuitPython_LTR559>
  - [datasheet](https://optoelectronics.liteon.com/upload/download/DS86-2013-0003/LTR-559ALS-01_DS_V1.pdf)


PDM-Micro
---------

  - Measures 
  - Status: implemented
  - I2C-Breakout: (Adafruit  ????)[https://adafru.it/????]
  - Address: 
  - Guide: 
  - CircuitPython-driver:
  - [datasheet]()


Please note that many of the Adafruit versions of the above sensors are
fitted with an LED. For some sensors, this can be disabled by cutting
a track, but for others you just have to destroy them.
