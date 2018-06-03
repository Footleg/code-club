#!/usr/bin/env python3

# Copyright (c) 2018 Paul Fretwell
# Author: @drfootleg
#
# Requires the Adafruit Capacitive Touch HAT Python libraries. See install instructions here:
# https://learn.adafruit.com/mpr121-capacitive-touch-sensor-on-raspberry-pi-and-beaglebone-black/software
#
# Based on the example code provided by Adafruit industries, written by Tony DiCola (2014).
# See the Adafruit examples/simpletest.py in the library download for license details of Adafruit code.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys

# Set this path to point to the location you installed the Adafruit_Python_MPR121 libraries
sys.path.append('/home/pi/Adafruit_Python_MPR121/')

import time
from psonic import send_message

import Adafruit_MPR121.MPR121 as MPR121

#Set true to see debug output of actual touch values
debug = True

def playSample(i):
    """ Method to broadcast an OSC message for each touch pad.
        Set the Sonic Pi sample names you want to be played in this method.
    """
    if i == 0:
        send_message("/play/choir")
    elif i == 1:
        send_message("/play/kick")
    elif i == 2:
        send_message("/play/voxyhit")
    elif i == 3:
        send_message("/play/scratch")
    elif i == 4:
        send_message("/play/drop")
    elif i == 5:
        send_message("/play/snaredub")
    elif i == 6:
        send_message("/play/cymbal")
    elif i == 7:
        send_message("/play/bong")
    elif i == 8:
        send_message("/play/triangle")
    elif i == 9:
        send_message("/play/twang")
    elif i == 10:
        send_message("/play/bell")
    else:
        send_message("/play/rewind")


def showTouchPadValues():
    # Display actual values from touch pads for debuggin sensitivity
    if debug:
        print('\t\t\t\t\t\t\t\t\t\t\t\t\t 0x{0:0X}'.format(cap.touched()))
        filtered = [cap.filtered_data(i) for i in range(12)]
        print('Filt:', '\t'.join(map(str, filtered)))
        base = [cap.baseline_data(i) for i in range(12)]
        print('Base:', '\t'.join(map(str, base)))


#Start main program execution
print('Adafruit MPR121 Capacitive Touch HAT Sonic Pi Sample Player')

# Create MPR121 instance.
cap = MPR121.MPR121()

# Initialize communication with MPR121 using default I2C bus of device, and
# default I2C address (0x5A).  On BeagleBone Black will default to I2C bus 0.
if not cap.begin():
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)

#Uncomment to manually set thresholds for your hardware configuration
#touch = 100
#release = 200
#cap.set_thresholds(touch,release)

# Main loop to print a message every time a pin is touched.
print('Press Ctrl-C to quit.')
last_touched = cap.touched()
while True:
    current_touched = cap.touched()
    # Check each pin's last and current state to see if it was pressed or released.
    for i in range(12):
        # Each pin is represented by a bit in the touched value.  A value of 1
        # means the pin is being touched, and 0 means it is not being touched.
        pin_bit = 1 << i
        # First check if transitioned from not touched to touched.
        if current_touched & pin_bit and not last_touched & pin_bit:
            print('{0} touched!'.format(i))
            showTouchPadValues()
            playSample(i)
        # Next check if transitioned from touched to not touched.
        if not current_touched & pin_bit and last_touched & pin_bit:
            print('{0} released!'.format(i))
            showTouchPadValues()
    # Update last state and wait a short period before repeating.
    last_touched = current_touched
    time.sleep(0.05)
