# ------------__ Hacking STEM – glove.py – micro:bit __-----------
# For use with the Lesson plan available 
# from Microsoft Education Workshop at http://aka.ms/hackingSTEM
#
#  Overview:
#  This code is one half of the Robotic Hand project. It detects analog voltage 
#  levels which correspond to deformation of velostat flex sensors attached to
#  the Glove protion of the lesson. It then transmits that data over radio to the 
#  Robotic Hand. We use 2 micro:bits in this project since the each board only 
#  supports up to 6 analog/pwm pins.
#  
#  Pins:
#  0: Thumb
#  1: Index Finger
#  2: Middle Finger
#  3: Ring Finger
#  4: Pinky
#
#  This project uses a BBC micro:bit microcontroller, information at:
#  https://microbit.org/ 
#
#  Comments, contributions, suggestions, bug reports, and feature
#  requests are welcome! For source code and bug reports see:
#  http://github.com/[TODO github path to Hacking STEM]
#
#  Copyright 2018, Adi Azulay
#  TODO add Arduino copyright and CC license
#  Microsoft EDU Workshop - HackingSTEM
#  MIT License terms detailed in LICENSE.txt
# ===---------------------------------------------------------------===

from microbit import *
import radio

# Setup & Config
display.off()  # Turns off LEDs to free up additional input pins
uart.init(baudrate=9600)  # Sets serial baud rate
radio.on() # Turn on radio
DATA_SPEED = 10 # Frequency of code looping
EOL = '\n' # End of Line Character
chan = 0 # Defualt channel number for radio
radio.config(length=64, channel=chan)

# Keeping a record of the min and max values allows to scale our readings to 
# the full range of 0-100.
min_max_array = [[1023,0], [1023,0], [1023,0], [1023,0], [1023,0]]

def smooth(pin):
    # Takes the average of 160 readings to elimniate any spikes.
    total = 0
    for i in range(0,160):
        raw_read = pin.read_analog()
        total = total + raw_read
    return total / 160

def scale(value, inMin, inMax, outMin, outMax):
    # Remaps a value from one min/max range to a different min/max range
    return (value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

def get_sensor_value(pin, pos):
    # Read voltage from pin, check whether the min/max array needs update, 
    # remap value from 0 -100
    global min_max_array
    sensor_value = smooth(pin)
    if (sensor_value < min_max_array[pos][0]):
        min_max_array[pos][0] = sensor_value
    if (sensor_value > min_max_array[pos][1]):
        min_max_array[pos][1] = sensor_value
    try:
        sensor_value = scale(sensor_value, min_max_array[pos][0], min_max_array[pos][1], 0, 100)
    except:
        return 0
    return sensor_value

#=============================================================================#
#------------------------------Main Program Loop------------------------------#
#=============================================================================#
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

    # Read each sensor and save that vaule to a new variable
    thumb_read = get_sensor_value(pin0, 0)
    index_read = get_sensor_value(pin1, 1)
    middle_read = get_sensor_value(pin2, 2)
    ring_read = get_sensor_value(pin3, 3)
    pinky_read = get_sensor_value(pin4, 4)
    # Send data to radio
    radio.send("{},{},{},{},{}".format(thumb_read, index_read, middle_read, ring_read, pinky_read))
    # Write data to serial, uart is how you call serial on micro:bit
    uart.write("{},{},{},{},{}".format(thumb_read, index_read, middle_read, ring_read, pinky_read))
   
