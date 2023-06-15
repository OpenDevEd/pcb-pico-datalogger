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

# configuration settings
HAVE_PCB     = True
HAVE_SD      = False
HAVE_DISPLAY = 'Inky-Pack'         # 'Inky-Pack', 'Display-Pack' or None
HAVE_LORA    = False

# hardware configuration settings for sensors
HAVE_AHT20   = True
HAVE_LTR559  = False
HAVE_MCP9808 = False
HAVE_ENS160  = False
HAVE_MIC_PDM_MEMS = False
HAVE_BH1750  = False

# Not implemented yet
HAVE_SHT45   = False
HAVE_BH1745  = False
HAVE_MIC_I2S_MEMS = False

# Logger identification constants
LOGGER_NAME  = 'Darasa Kamili'  # Perfect Classroom
LOGGER_ID    = '000'            # Change this to your logger id
LOGGER_LOCATION = '6G5X46G4+XQ' # Plus Code for Dar airport
LOGGER_TITLE = LOGGER_NAME + " " + LOGGER_LOCATION
