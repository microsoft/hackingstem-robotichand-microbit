
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

# servoPin = [pin0, pin1, pin2, pin3, pin4]
# fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']
# for i in servoPin:
#     fingers[0] = servo(i)

minMaxArray = [[1023,0], [1023,0], [1023,0], [1023,0], [1023,0]]


smoothingArray = [0] * 5
for i in range(5):
    smoothingArray[i] = [511] * 16

thumb = servo(pin0)
index = servo(pin1)
middle = servo(pin2)
ring = servo(pin3)
pinky = servo(pin4)

def driveServos(t, i, m, r, p):
    thumb.angle(t)
    index.angle(i)
    middle.angle(m)
    ring.angle(r)
    pinky.angle(p)

    # Print Voltage , Current
    # uart.write('{},{}'.format(voltage, current)+EOL)

    # Sleep for the dataSpeed before looping the code

def scale(value, inMin, inMax, outMin, outMax):
    return (value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

def smooth(pin, pos):
    # total = 0
    # smoothingArray[pos].insert(0, pin.read_analog())
    # smoothingArray[pos].pop(16)
    # for i in range(16):
    #     val = smoothingArray[pos][i]
    #     total = total + val
    # return total / 16
    total = 0
    for i in range(0,160):
        rawRead = pin.read_analog()
        total = total + rawRead
    return total / 160


def getSensorValue(pin, pos):
    global minMaxArray
    sensorValue = smooth(pin, pos)
    print("val: {}".format(sensorValue))
    if (sensorValue < minMaxArray[pos][0]):
        minMaxArray[pos][0] = sensorValue
    print("min: {}".format(minMaxArray[pos][0]))
    if (sensorValue > minMaxArray[pos][1]):
        minMaxArray[pos][1] = sensorValue
    print("max: {}".format(minMaxArray[pos][1]))
    try:
        sensorValue = scale(sensorValue, minMaxArray[pos][0], minMaxArray[pos][1], 0, 100)
    except:
        return 0
    return sensorValue

def readSensors():
    thumbRead = scale(getSensorValue(pin0, 0), 0, 100, 5, 175)
    print(thumbRead)
    indexRead = getSensorValue(pin1, 1)
    middleRead = getSensorValue(pin2, 2)
    ringRead = getSensorValue(pin3, 3)
    pinkyRead = getSensorValue(pin4, 4)
    
    driveServos(thumbRead, indexRead, middleRead, ringRead, pinkyRead)
    sleep(1000)
    

while True:
    readSensors()