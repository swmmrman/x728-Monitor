#!/usr/bin/env python3

import struct
import smbus
import time
import RPi.GPIO as GPIO
import sys
import os

bus = smbus.SMBus(1) # setup the SMBus to read from.

PINS = {
    'AC': 6, # AC detection pin, High when external power is lost.
    'BOOT': 12, #Pin to signal the pi as running
    'OFF': 13, #Pin to signal we are shutting down
}
