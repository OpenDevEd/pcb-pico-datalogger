Hardware setup
--------------

To set up the board, you should:
* Connect AA batteries (or similar) via the battery port
* Add a coin cell to maintain data on the RTC (CR2032)
* Remove the jumper between the Pico and the coin cell
* Connect the Pico via USB cable to laptop

The put circuitpython on to the Raspberry Pi
* If you have a Pico, install https://circuitpython.org/board/raspberry_pi_pico/
* If you have a Pico W, install https://circuitpython.org/board/raspberry_pi_pico_w/

Them copy contents of the src folder onto the Pico.

When you're done with software installation
* Unplug the USB cable
* Replace the jumper

Note that if you want to update software in the future, remove the jumper first.
