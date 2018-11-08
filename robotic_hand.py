# ------------__ Hacking STEM – robotic_hand.py – micro:bit __-----------
# For use with the Machines That Emulate Humans lesson plan available 
# from Microsoft Education Workshop at http://aka.ms/hackingSTEM
#
#  Overview:
#  This code is one half of the Robotic Hand project. It controls servo motors 
#  on the hand portion using numbers recived over radio from the Glove portion 
#  of the project. We use 2 micro:bits in this project since the each board 
#  only supports up to 6 analog/pwm pins.
#
#  This project uses a BBC micro:bit microcontroller, information at:
#  https://microbit.org/
#
#  Comments, contributions, suggestions, bug reports, and feature
#  requests are welcome! For source code and bug reports see:
#  http://github.com/[TODO github path to Hacking STEM]
# 
#  Servo Code Copyright (c) 2016 Microbit Playground
#  TODO add Arduino copyright and CC license
#  Copyright 2018, Adi Azulay
#  Microsoft EDU Workshop - HackingSTEM
#  MIT License terms detailed in LICENSE.txt
# ===---------------------------------------------------------------===

from microbit import *
import radio

# This class adds servo controls to micro:bit
class servo:
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

#TODO remove?
# minMaxArray = [[1023,0], [1023,0], [1023,0], [1023,0], [1023,0]]

# smoothingArray = [0] * 5
# for i in range(5):
#     smoothingArray[i] = [511] * 16

# Create servo objects for each finger
thumb = servo(pin0)
index = servo(pin1)
middle = servo(pin2)
ring = servo(pin3)
pinky = servo(pin4)

def scale(value, inMin, inMax, outMin, outMax):
    # Remaps a value from one min/max range to a different min/max range
    return (value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

# def getSensorValue(pin, pos):
#     global minMaxArray
#     sensorValue = smooth(pin, pos)
#     print("val: {}".format(sensorValue))
#     if (sensorValue < minMaxArray[pos][0]):
#         minMaxArray[pos][0] = sensorValue
#     print("min: {}".format(minMaxArray[pos][0]))
#     if (sensorValue > minMaxArray[pos][1]):
#         minMaxArray[pos][1] = sensorValue
#     print("max: {}".format(minMaxArray[pos][1]))
#     try:
#         sensorValue = scale(sensorValue, minMaxArray[pos][0], minMaxArray[pos][1], 0, 100)
#     except:
#         return 0
#     return sensorValue

# def run_code():
#     thumbRead = scale(pin0.read_analog(), 0, 1023, 0, 100)
#     thumb.angle(thumbRead)

# The main program loop
while True:
    # Changes the radio channel
    if button_a.is_pressed() and chan != 0:
        chan -= 1
        radio.config(channel=chan)
        display.on()
        display.show(chan, delay=500)
        sleep(600)
        display.off()
    elif button_b.is_pressed() and chan < 83:
        chan += 1
        radio.config(channel=chan)
        display.on()
        display.show(chan, delay=500)
        sleep(600)
        display.off()
    
    # Listen for radio data
    data_in = radio.receive() 
    
    # Seperate the incoming radio data
    if(data_in):
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