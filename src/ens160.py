#-----------------------------------------------------------------------------
# Sensor definition for ENS160.
#
# Naming convention:
#   - filenames in lowercase (ens160.py)
#   - class name the same as filename in uppercase (ENS160)
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

import adadruit_ens160

class ENS160:
  formats = ["Status:", "{0}",
             "AQI:", "{0}",
             "TVOC:", "{0} ppb",
             "eCO2:", "{0} ppm eq."
             ]
  headers = 'status,AQI,TVOC ppb,eCO2 ppm eq.'

  def __init__(self,config,i2c0=None,i2c1=None,spi0=None,spi1=None):
    """ constructor """
    try:
      if i2c1:
        self.ens160 = adafruit_ens160.ENS160(i21)
    except:
      if i2c0:
        self.ens160 = adafruit_ens160.ENS160(i21)

  def read(self,data,values):
    if "aht20" in data:
      self.ens160.temperature_compensation = data["aht20"]["temp"]
      self.ens160.humidity_compensation    = data["aht20"]["hum"]
    ens_data           = self.ens160.read_all_sensors()
    ens_data['status'] = self.ens160.data_validity

    data["ens160"] = ens_data
    values.extend([None,ens_data['status']])
    values.extend([None,ens_data['AQI']])
    values.extend([None,ens_data['TVOC']])
    values.extend([None,ens_data['eCO2']])
    return f"{ens_data['status']},{ens_data['AQI']},{ens_data['TVOC']},{ens_data['eCO2']}"
