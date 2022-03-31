#!/usr/bin/python3

import smbus
import time
import os
import sys
import x728
import RPi.GPIO as GPIO


def main():
    if(os.getuid() != 0):
        print("This must be run as root")
        sys.exit(1)
    GPIO.setmode(GPIO.BCM)
    for i in 6, 12, 26:
        GPIO.setup(i, GPIO.OUT)
    ups = x728.x728(2.1, smbus.SMBus(1))
    ups.call_shutdown()
    sys.exit(0)


main()
