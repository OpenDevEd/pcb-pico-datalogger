#-----------------------------------------------------------------------------
# Configuration constants for main.py.
#
# !!! This file is not maintained within Github !!!
#
# Author: Bernhard Bablok
#
# Website: https://github.com/pcb-pico-datalogger
#-----------------------------------------------------------------------------

TEST_MODE   = True        # set to FALSE for a production setup
NET_UPDATE  = True        # update RTC from time-server if time is invalid
OFF_MINUTES = 1           # turn off for x minutes
BLINK_TIME_START  = 0.5   # blink time of LED before start of data-collection
BLINK_TIME_END  = 0.25    # blink time of LED  after finish of data-collection
BLINK_START = 3           # blink n times before start of data-collection
BLINK_END   = 5           # blink n times after finish of data-collection

FORCE_CONT_MODE       = False      # Use continuous mode (with CONT_INT) even when on battery
FORCE_STROBE_MODE     = False      # Use strobe mode (with OFF_MINUTES) even when on power
CONT_INT              = 5          #  interval in continuous mode (in seconds)

# hardware setup
HAVE_PCB     = True       # The Pico is running on the pcb described here: https://github.com/pcb-pico-datalogger
HAVE_SD      = False      # The PCB has an sd card inserted (or an sd card is connected otherwise)
HAVE_DISPLAY = True       # The Pioco has a Pimoroni Pico Inky display connected (via PCB or otherwise)

# hardware configuration settings for sensors
HAVE_AHT20   = True       # Sense temperature and humidity with an Adafruit AHT20 sensor connected on I2C bus
HAVE_LTR559  = True       # Sense light level in lux with a Pimoroni LTR-559 sensor connected on I2C bus
HAVE_MCP9808 = True       # Sense temperature with a Adafruit MCP9808 sensor connected on I2C bus
HAVE_ENS160  = False      # Sense environmental properties with an ENS160 sensor connected on I2C bus
HAVE_MIC_PDM_MEMS = True  # Sense noise with a MIC-PDM-MEMS sensor connected via PDMio interface

# hardware configuration configuration settings - not implemented yet
HAVE_LORA    = False      # Adafruit RFM96W LoRa Radio Transceiver Breakout is avaialble
HAVE_SHT45   = False      # Sense temperature and humidity with a SHT45 sensor connected on I2C bus
HAVE_BH1750  = False      # Sense light level with a BH1750 sensor connected on I2C bus
HAVE_BH1745  = False      # Sense light level with a BH1745 sensor connected on I2C bus
HAVE_AM2301B = False      # Sense temperature and humidity with Adafruit AM2301B Wired enclosed shell on I2C bus

# hardware configuration configuration settings - I2S mic not yet supported in Circuitpython
HAVE_MIC_I2S_MEMS = False # Sense noise with a MIC-I2S-MEMS sensor connected on I2


# Logger identification constants
LOGGER_NAME  = 'Darasa Kamili'  # Perfect Classroom
LOGGER_ID    = '000'            # Change this to your logger id
LOGGER_LOCATION = '6G5X46G4+XQ' # Plus Code for Dar airport
LOGGER_TITLE = LOGGER_NAME + " " + LOGGER_LOCATION
