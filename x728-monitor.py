#!/usr/bin/env python3

import struct
import smbus
import time
import RPi.GPIO as GPIO
import sys
import os


def power_changed(channel):
    global AC_OUT, time_left, TIMEOUT
    current_time = time.asctime()
    if GPIO.input(PINS['AC']):
        AC_OUT = True
        print(
            F"{current_time}: X728: Power Lost\n"
            F"Starting power off countdown\n"
            F"{TIMEOUT}: seconds until shutdown\n"
        )
    else:
        AC_OUT = False
        print(F"{current_time}: Power Restored")
        time_left = TIMEOUT


def get_voltage(bus):
    address = 0x36  # Address of the Battery gauge.
    data_big_e = bus.read_word_data(address, 2)
    # Convert from big to little endian
    data_little_e = struct.unpack("<H", struct.pack(">H", data_big_e))[0]
    # convert value to Voltage, numbers from manufacturer.
    voltage = data_little_e * 1.25 / 1000 / 16
    return voltage


def call_shutdown():
    GPIO.output(PINS['OFF'], GPIO.HIGH)  # Set shutdown pin high.
    time.sleep(4)  # 4 seconds to signal we are shutting down the X728
    GPIO.output(PINS['OFF'],  GPIO.LOW)  # Set back low to prevent forced off.
    print(F"{time.asctime()}:X728 Shutting down...")
    os.system('poweroff')
    # GPIO.cleanup()
    # sys.exit(0) # Exit out.


# Global settings
PINS = {
    'AC': 6,  # AC detection pin, High when external power is lost.
    'BOOT': 12,  # Pin to signal the pi as running
    # Pin to signal we are shutting down
    # GPIO is 26 for x728 v2.0, GPIO is 13 for X728 v1.2/v1.3
    'OFF': 26,
}
TIMEOUT = 30
time_left = TIMEOUT


def main():
    if(os.getuid() != 0):
        print("This must be run as root")
        sys.exit(1)
    global time_left, AC_OUT
    MIN_VOLTS = 3.5
    bus = smbus.SMBus(1)  # setup the SMBus to read from.
    GPIO.setwarnings(False)  # disable incase of relaunch.
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PINS['AC'], GPIO.IN)  # AC detect pin is read only
    GPIO.setup(PINS['BOOT'], GPIO.OUT)
    GPIO.setup(PINS['OFF'], GPIO.OUT)
    # Set boot pin high to indicate we are running
    GPIO.output(PINS['BOOT'], GPIO.HIGH)

    AC_OUT = GPIO.input(PINS['AC'])
    GPIO.add_event_detect(PINS['AC'], GPIO.BOTH, callback=power_changed)

    # warning, ugly code (I've never touched python)
    # shut down when power is out after x seconds.
    # Shut down immediately if power out and batt is low
    while True:
        time.sleep(1)
        if AC_OUT:
            volts = get_voltage(bus)
            time_left -= 1
            if time_left <= 0 or volts < MIN_VOLTS:
                call_shutdown()


if __name__ == "__main__":
    main()
