#-----------------------------------------------------------------------------
# Pico initialization file after hard reset. This file will check if
# GP12 is low (i.e. button SW-A is pressed) and enter admin-mode by
# restarting into admin.py.
#
# Author: Bernhard Bablok
#
# Website: https://github.com/pcb-pico-datalogger
#-----------------------------------------------------------------------------

import board
import supervisor
from digitalio import DigitalInOut, Pull, Direction

# --- pin-constants (don't change unless you know what you are doing)   ------

PIN_SWA = board.GP12  # for both Inky-Pack and Display-Pack

# --- configure hardware   ---------------------------------------------------

switch_a = DigitalInOut(PIN_SWA)
switch_a.direction = Direction.INPUT
switch_a.pull = Pull.UP

# --- check if switch A is pressed and if so, enter admin-mode   -------------

if not switch_a.value:
  supervisor.set_next_code_file("admin.py",sticky_on_reload=True)
  supervisor.reload()
