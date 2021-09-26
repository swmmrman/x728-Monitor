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
        print(F"{current_time}: Power Restored")


def get_voltage(bus):
    address = 0x36 # Address of the Battery gauge.
    data_big_e = bus.read_word_data(address, 2)
    #Convert from big to little endian
    data_little_e= struct.unpack("<H", struct.pack(">H", data_big_e))[0]
    #convert value to Voltage, numbers from manufacturer.
    voltage = data_little_e * 1.25 / 1000 / 16
    return voltage


def call_shutdown():
    GPIO.output(PINS['OFF'], 1) # Set shutdown pin high.
    time.sleep(4) # 4 seconds to signal we are shutting down the X728
    GPIO.output(PINS['OFF'], 0) # Set back low to prevent forced off.
    os.system('shutdown now')
    GPIO.cleanup()
    sys.exit(0) # Exit out.

bus = smbus.SMBus(1) # setup the SMBus to read from.

PINS = {
    'AC': 6, # AC detection pin, High when external power is lost.
    'BOOT': 12, #Pin to signal the pi as running
    'OFF': 13, #Pin to signal we are shutting down
}
MIN_VOLTS = 3.5

GPIO.setwarnings(False) #disable incase of relaunch.
GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS['AC'], GPIO.IN) #AC detect pin is read only
GPIO.setup(PINS['BOOT'], GPIO.OUT)
GPIO.setup(PINS['OFF'], GPIO.OUT)
GPIO.output(PINS['BOOT'], 1) # Set boot pin high to indicate we are running

AC_OUT = GPIO.input(PINS['AC'])
GPIO.add_event_detect(PINS['AC'], GPIO.BOTH, callback=power_changed)

# warning, ugly code (I've never touched python)
# shut down when power is out after x seconds.  Shut down immediately if power out and batt is low
while True:
    time.sleep(1)
    if AC_OUT:
        current_time = time.asctime()
        print(F"{current_time}:Starting power off countdown")
        timeout = 30 #seconds
        while AC_OUT:
            print(F"{timeout}:tic")    
            volts = get_voltage(bus)
            timeout -= 1
            if timeout <= 0 or volts < MIN_VOLTS:
                call_shutdown()
            else:
                time.sleep(1)

