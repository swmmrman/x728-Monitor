#!/usr/bin/env python3

import struct
import smbus
import time
import RPi.GPIO as GPIO
import sys
import os

bus = smbus.SMBus(1) # setup the SMBus to read from.

PINS = {
    'AC': 6,
    'BOOT': 12,
    'OFF': 13,
}
