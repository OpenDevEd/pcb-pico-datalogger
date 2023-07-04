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
BLINK_TIME_START  = 0.5   # blink time of LED before start of data-collection
BLINK_TIME_END  = 0.25    # blink time of LED  after finish of data-collection
BLINK_START = 3           # blink n times before start of data-collection
BLINK_END   = 5           # blink n times after finish of data-collection

NET_UPDATE  = True        # update RTC from time-server if time is invalid

OFF_MINUTES = 1           # turn off for x minutes

# time table: one entry per day (starting with Monday)
#             ((h_start,h_end,h_inc),(m_start,m_end,m_inc))
# The example has Mo-Fr from 07:00-17:45 every 15 minutes
#TIME_TABLE = [
#  ((7,18,1),(0,59,15)),
#  ((7,18,1),(0,59,15)),
#  ((7,18,1),(0,59,15)),
#  ((7,18,1),(0,59,15)),
#  ((7,18,1),(0,59,15)),
#  (None,None),
#  (None,None)
#  ]

FORCE_CONT_MODE       = False      # Use continuous mode (with CONT_INT) even when on battery
FORCE_STROBE_MODE     = False      # Use strobe mode (with OFF_MINUTES) even when on power
CONT_INT              = 60         #  interval in continuous mode (in seconds)

# hardware setup
HAVE_I2C0    = False               # also use second I2C-bus
HAVE_PCB     = True                # The Pico is running on the pcb described here: https://github.com/pcb-pico-datalogger
HAVE_SD      = False               # The PCB has an sd card inserted (or an sd card is connected otherwise)
CSV_FILENAME = "/sd/log_{ID}_{YMD}.csv"
HAVE_DISPLAY = 'Inky-Pack'         # 'Inky-Pack', 'Display-Pack' or None
HAVE_LORA    = False               # Adafruit RFM96W LoRa Radio Transceiver Breakout is avaialble

# hardware configuration settings for sensors
SENSORS = "id battery"             # list of sensors. Each needs a <sensor>.py file

SHOW_UNITS = False # Show units in the csv output

# Logger identification constants
LOGGER_NAME  = 'Darasa Kamili'  # Perfect Classroom
LOGGER_ID    = '000'            # Change this to your logger id
LOGGER_LOCATION = '6G5X46G4+XQ' # Plus Code for Dar airport
LOGGER_TITLE = LOGGER_NAME + " " + LOGGER_LOCATION

# font for the display
FONT_DISPLAY     = 'DejaVuSansMono-Bold-18-subset'
