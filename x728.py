#!/usr/bin/env python3
import struct
import smbus
import RPi.GPIO as GPIO

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


def get_capacity(bus):
    address = 0x36 #address of battery gauge.
    data_big_e = bus.read_word_data(address, 4)
    #change the endian to little
    data_little_e = struct.unpack("<H", struct.pack(">H", data_big_e))[0]
    #convert value to capacity, numbers from manufacturer
    capacity = data_little_e / 256
    return capacity


def call_shutdown():
    GPIO.output(PINS['OFF'], 1) # Set shutdown pin high.
    time.sleep(4) # 4 seconds to signal we are shutting down the X728
    GPIO.output(PINS['OFF'], 0) # Set back low to prevent forced off.
    os.system('shutdown now')
    GPIO.cleanup()
    sys.exit(0) # Exit out.


PINS = {
    'AC': 6, # AC detection pin, High when external power is lost.
    'BOOT': 12, #Pin to signal the pi as running
    'OFF': 13, #Pin to signal we are shutting down
}
