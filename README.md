Pico Datalogger with Integrated Power-Management
================================================

This is a breakout supporting low-frequency data-logging with a Raspberry Pi Pico.

![](pcb1.jpg)

Core functions:
  * log data to a micro-sd card;
  * software-controlled power-control with very low standby current.

From a technical viewpoint the breakout allows you to
  * turn on the system using a button or
  * use a RTC-alarm to trigger wakup,
  * turn off the system using a dedicated digital-io,
  * power the system from a lipo or battery-pack,
  * keep time using a coincell backup-battery even if the board is not powered.


Hardware Components
-------------------

Time-keeping uses the PCF8523 RTC with integrated support for a backup-battery.

![](pcb2.jpg)

Power management uses a D-type flip-flop which drives the enable pin of the Pico.
In "reset"-state, the enable pin is pulled high and the Pico is running. The
reset is triggered either by a button, or by an RTC-alarm.

The "done"-pin of the Pico is connected to the CLK-pin of the flip-flop. A rising edge
will toggle the enable pin.

A micro-sd card reader is connected to SPI to enable logging of data.

Various additional connectors allow the user to connect sensors or displays.


Software
--------

A CircuitPython implementation for a datalogger-program is in the directory
`src`. See [datalogger.md](datalogger.md) for details.


Background
----------

For background on / motivation for this project, please see
<https://opendeved.net/programmes/ilce-in-tanzania/>.


Additional resources
--------------------

  * [hardware_setup.md](hardware_setup.md)
  * [KiCAD design-files](pico-datalogger/)
  * [Pinout](pins.md)
  * Case for this PCB: https://github.com/OpenDevEd/case-for-pico-datalogger-rev0.98


License
-------

Software in `src` is licensed under the GPL3. Hardware is licensed by:

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International
License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]:
https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
