# Introduction

Micropython code for Microsoft Hacking STEM Sensorized Glove and Robotic Hand projects and the Machines That Emulate Humans lesson plan adapted for micro:bit

**Note** that this project is designed to use 2 micro:bits since each board only supports up to 6 analog/pwm pins.

* glove.py
  * Captures the analog signals from the flex sensors and transmits this data over radio to the Robotic Hand micro:bit
* robotic_hand.py
  * Receives data from the Glove micro:bit and controls the servos in the mechanical hand.

## Getting Started

1. Download lesson assets at https://education.microsoft.com/hackingStem/lesson/20647903
1. Build your Sensorized Glove and Robotic Hand!
1. Use [Mu](https://codewith.mu/) to flash glove.py to your glove [micro:bit](https://microbit.org/) microcontroller
1. Use [Mu](https://codewith.mu/) to flash robotic_hand.py to your hand [micro:bit](https://microbit.org/) microcontroller
1. Verify data interactions in Excel from (hand microcontroller)
1. Ready, Set, Science!

### Connecting the two micro:bits

To support radio communication both glove and robotic_hand micro:bits must be on the same radio channel for this to work.

#### Setting Radio Channels

* Press both buttons until a number appears. This is the channel number (0 by default)
* Set the number by pressing the A dna B buttons to increase or decrease the channel number
* Do this each pair of micro:bits

Note that if there are multiple projects going on in the same room choose a unique channel number for each glove/robotic_hand pair to ensure that it is you who controls your robotic hand!

## Microsoft Data Streamer Resources

1. https://aka.ms/data-streamer-developer
1. https://aka.ms/data-streamer

## Make it your own!

This project is licensed under the MIT open source license, see License. The MIT license allows you to take this project and make awesome things with it! MIT is a very permissive license, but does require you include license and copyright from LICENSE in any derivative work for sake of attribution.

Fork away! Let us know what you build!

http://aka.ms/hackingSTEM
