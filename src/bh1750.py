#-----------------------------------------------------------------------------
# Sensor definition for BH1750.
#
# Naming convention:
#   - filenames in lowercase (bh1750.py)
#   - class name the same as filename in uppercase (BH1750)
#   - the constructor must take five arguments (config,i2c0,ic1,spi0,spi1)
#     and probe for the device
#   - i2c1 is the default i2c-device and should be probed first
#   - the read-method must update the data and return a string with the
#     values for the csv-record
#
# Author: Bernhard Bablok
#
# Website: https://github.com/pcb-pico-datalogger
#-----------------------------------------------------------------------------

from log_writer import Logger
g_logger = Logger()

import adafruit_bh1750

class BH1750:
  formats = ["L/bhx0:", "{0:.0f}lx"]
  headers = 'L/bhx0 lx'

  def __init__(self,config,i2c0=None,i2c1=None,spi0=None,spi1=None):
    """ constructor """

    try:
      if i2c1:
        g_logger.print("testing bh1750 on i2c1")
        self.bh1750 = adafruit_bh1750.BH1750(i2c1)
        g_logger.print("detected bh1750 on i2c1")
    except Exception as ex:
      g_logger.print(f"exception: {ex}")
      if i2c0:
        g_logger.print("testing bh1750 on i2c0")
        self.bh1750 = adafruit_bh1750.BH1750(i2c0)
        g_logger.print("detected bh1750 on i2c0")

  def read(self,data,values):
    lux = self.bh1750.lux
    data["bh1750"] = {
      "lux": lux
    }
    values.extend([None,lux])
    return f"{lux:.0f}"
