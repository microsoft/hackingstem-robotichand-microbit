# ------------__ Hacking STEM - robotic_hand.py - micro:bit __-----------
# For use with the Lesson plan available
# from Microsoft Education Workshop at
# https://education.microsoft.com/hackingStem/lesson/20647903
# http://aka.ms/hackingSTEM
#
#  Overview:
#  This code is one half of the Robotic Hand project, the other half is
#  glove.py. It controls servo motors on the hand portion using numbers received
#  over radio from the Glove portion of the project. We use 2 micro:bits in
#  this project since the each board only supports up to 6 analog/pwm pins.
#
#  Pins:
#  0: Thumb Servo
#  1: Index Finger Servo
#  2: Middle Finger Servo
#  3: Ring Finger Servo
#  4: Pinky Servo
#
#  Radio Channels:
#  You can change the radio channel on your micro:bit using Button A to cycle
#  down and Button B to cycle up in numbers.
#  Note: When changing channels the motors may twitch a bit.
#
#  This project uses a BBC micro:bit microcontroller, information at:
#  https://microbit.org/
#
#  Comments, contributions, suggestions, bug reports, and feature
#  requests are welcome! For source code and bug reports see:
#  https://github.com/microsoft/hackingstem-robotichand-microbit
# 
#  Copyright 2018, Adi Azulay
#  Microsoft EDU Workshop - HackingSTEM
#  Servo Code Copyright (c) 2016 Microbit Playground
#
#  MIT License terms detailed in LICENSE.txt
# ===---------------------------------------------------------------===

from microbit import *
import radio

class servo:
    # This class adds servo controls to micro:bit
    def __init__(self, pinNumber, freq=50, min_micro_s=500, max_micro_s=2400, angle=180):
        # Initilize a servo motor
        self.pin = pinNumber
        self.min_micro_s = min_micro_s
        self.max_micro_s = max_micro_s
        self.micro_s = 0
        self.analog_period = 0
        self.angle = angle
        self.freq = freq
        analog_period = round((1/self.freq) * 1000)  # hertz to miliseconds
        self.pin.set_analog_period(analog_period)

    def write_us(self, micro_s):
        # Determines the width of the PWM wave
        micro_s = min(self.max_micro_s, max(self.min_micro_s, micro_s))
        duty = round(micro_s * 1024 * self.freq // 1000000)
        self.pin.write_analog(duty)
    
    def write_angle(self, degrees=None):
        # Converts degrees to micro seconds
        degrees = degrees % 360
        total_range = self.max_micro_s - self.min_micro_s
        micro_s = self.min_micro_s + total_range * degrees // self.angle
        self.write_us(micro_s)

# Setup & Config
display.off()  # Turns off LEDs to free up additional input pins
uart.init(baudrate=9600)  # Sets serial baud rate
radio.on() # Turns on radio
DATA_SPEED = 10 # Frequency of code looping
EOL = '\n' # End of Line Character
chan = 0 # Defualt channel number for radio
radio.config(length=64, channel=chan)

# Create servo objects for each finger
thumb = servo(pin0)
index = servo(pin1)
middle = servo(pin2)
ring = servo(pin3)
pinky = servo(pin4)

def scale(value, inMin, inMax, outMin, outMax):
    # Remaps a value from one min/max range to a different min/max range
    return (value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

#=============================================================================#
#------------------------------Main Program Loop------------------------------#
#=============================================================================#
while True:    
    # Changes the radio channel
    while button_a.is_pressed() and chan != 0:
        chan -= 1
        radio.config(channel=chan)
        display.on()
        display.show(chan, delay=500)
        sleep(600)
        display.off()
    while button_b.is_pressed() and chan < 83:
        chan += 1
        radio.config(channel=chan)
        display.on()
        display.show(chan, delay=500)
        sleep(600)
        display.off()
    
    # Listen for radio data
    data_in = radio.receive()
    
    # Seperate the incoming radio data
    if (data_in):
        parsed_data = data_in.split(",")

    # Scale the incoming data to degrees for servo rotation
    if (data_in):
        thumb_read = scale(float(parsed_data[0]), 0, 100, 5, 175)
        thumb.write_angle(thumb_read)
        index_read = scale(float(parsed_data[1]), 0, 100, 5, 175)
        index.write_angle(index_read)
        middle_read = scale(float(parsed_data[2]), 0, 100, 5, 175)
        middle.write_angle(middle_read)
        ring_read = scale(float(parsed_data[3]), 0, 100, 5, 175)
        ring.write_angle(ring_read)
        pinky_read = scale(float(parsed_data[4]), 0, 100, 5, 175)
        pinky.write_angle(pinky_read)
        # first 4 channels are for unimplemented functionality
        uart.write("0,0,0,0," + data_in + EOL)