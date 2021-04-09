#!/usr/bin/env python3

import struct
import smbus
import time
import RPi.GPIO as GPIO
import sys
import os

def power_changed(channel):
    global AC_OUT
    current_time = time.asctime()
    if GPIO.input(PINS['AC']):
        AC_OUT = True
        print(F"{current_time}: Power Lost")
    else:
        AC_OUT = False
        print(F"{current_time} Power Restored")


bus = smbus.SMBus(1) # setup the SMBus to read from.

PINS = {
    'AC': 6, # AC detection pin, High when external power is lost.
    'BOOT': 12, #Pin to signal the pi as running
    'OFF': 13, #Pin to signal we are shutting down
}

GPIO.setwarning(False) #disable incase of relaunch.
GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS['AC'], GPIO.IN) #AC detect pin is read only
GPIO.setup(PINS['BOOT', GPIO.OUT])
GPIO.setup(PINS['OFF'])
GPIO.output(PINS['BOOT'], 1) # Set boot pin high to indicate we are running

AC_OUT = GPIO.input(PINS['AC'])
GPIO.add_event_detect(PINS['AC', GPIO.BOTH, callback=power_changed])
