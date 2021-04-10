#!/usr/bin/env python3
import struct
import smbus
import RPi.GPIO as GPIO

def get_voltage(bus):
    address = 0x36 # Address of the Battery gauge.
    data_big_e = bus.read_word_data(address, 2)
    #Convert from big to little endian
    data_little_e= struct.unpack("<H", struct.pack(">H", data_big_e))[0]
    #convert value to Voltage, numbers from manufacturer.
    voltage = data_little_e * 1.25 / 1000 / 16
    return voltage
