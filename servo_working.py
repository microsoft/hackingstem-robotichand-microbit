# ------------__ Hacking STEM – seismograph.py – micro:bit __-----------
# For use with the Lesson plan available 
# from Microsoft Education Workshop at http://aka.ms/hackingSTEM
#
#  Overview:
#
#  This project uses a BBC micro:bit microcontroller, information at:
#  https://microbit.org/
#
#  Comments, contributions, suggestions, bug reports, and feature
#  requests are welcome! For source code and bug reports see:
#  http://github.com/[TODO github path to Hacking STEM]
#
#  Copyright 2018, Adi Azulay
#  Microsoft EDU Workshop - HackingSTEM
#  MIT License terms detailed in LICENSE.txt
# ===---------------------------------------------------------------===

from microbit import *

class servo:
    def __init__(self, pinNumber):
        pinNumber.set_analog_period(20)
        self.pin = pinNumber

    def angle(self, angle):
        self.pin.write_analog(angle)

# Frequency of code looping
dataSpeed = 10

# End of Line Character
EOL = '\n'

# Setup & Config
display.off()  # Turns off LEDs to free up additional input pins
uart.init(baudrate=9600)  # Sets serial baud rate

thumb = servo(pin0)

while True:
    thumb.angle(175)
    sleep(1000)
    thumb.angle(5)
    sleep(1000)