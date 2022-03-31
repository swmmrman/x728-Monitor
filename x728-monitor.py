#!/usr/bin/env python3

import configparser
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
            F"{TIMEOUT}: seconds until shutdown\n",
            flush=True
        )
    else:
        AC_OUT = False
        print(F"{current_time}: Power Restored\n", flush=True)
        time_left = -1 if TIMEOUT == 0 else TIMEOUT


def get_voltage(bus):
    address = 0x36  # Address of the Battery gauge.
    data_big_e = bus.read_word_data(address, 2)
    # Convert from big to little endian
    data_little_e = struct.unpack("<H", struct.pack(">H", data_big_e))[0]
    # convert value to Voltage, numbers from manufacturer.
    voltage = data_little_e * 1.25 / 1000 / 16
    return voltage


def get_capacity(bus):
    address = 0x36  # Address of the Battery gauge.
    data_big_e = bus.read_word_data(address, 4)
    # Convert from big to little endian
    data_little_e = struct.unpack("<H", struct.pack(">H", data_big_e))[0]
    return data_little_e / 256


def call_shutdown():
    GPIO.output(PINS['OFF'], GPIO.HIGH)  # Set shutdown pin high.
    time.sleep(4)  # 4 seconds to signal we are shutting down the X728
    GPIO.output(PINS['OFF'],  GPIO.LOW)  # Set back low to prevent forced off.
    print(F"{time.asctime()}:X728 Shutting down...", flush=True)
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
    'BUZZ': 20,
}

DEBUG = False
TIMEOUT = 30
time_left = TIMEOUT
ALERT_LEVEL = 100
ALERT_VOLTS = 4.2


def main():
    global time_left, AC_OUT, DEBUG, TIMEOUT, PINS
    if(os.getuid() != 0):
        print("This must be run as root", flush=True)
        sys.exit(1)
    conf_file = '/etc/x728.conf'
    config = configparser.ConfigParser()
    if not os.path.exists('/etc/x728.conf'):
        conf_file = 'x728.conf'
    config.read(conf_file)
    version = float(config['DEVICE']['version'].strip(';'))
    ALERT_LEVEL = float(config['PARAMETERS']['alert_level'].strip())
    ALERT_VOLTS = float(config['PARAMETERS']['alert_level'].strip())
    DEBUG = True if config['PARAMETERS']['debug'].strip() == "true" else False
    PINS['BUZZ'] = float(config['PARAMETERS']['buzzer'].split(" ")[0])
    if version < 2:
        PINS['OFF'] = 13  # Change if older x728
    TIMEOUT = int(config['PARAMETERS']['timeout'])
    time_left = -1 if TIMEOUT == 0 else TIMEOUT
    MIN_VOLTS = float(config['PARAMETERS']['min_volts'])
    MIN_CAPACITY = float(config['PARAMETERS']['min_capacity'])
    bus = smbus.SMBus(1)  # setup the SMBus to read from.
    GPIO.setwarnings(False)  # disable incase of relaunch.
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PINS['AC'], GPIO.IN)  # AC detect pin is read only
    GPIO.setup(PINS['BOOT'], GPIO.OUT)
    GPIO.setup(PINS['OFF'], GPIO.OUT)
    if PINS['BUZZ'] != 0:
        GPIO.setup(PINS['BUZZ'], GPIO.OUT)
    # Set boot pin high to indicate we are running
    GPIO.output(PINS['BOOT'], GPIO.HIGH)
    print(
        F"Board version: \t{version}\n"
        F"Shutdown Delay: \t{TIMEOUT}\n"
        F"Alert Volts:\t\t{ALERT_VOLTS}\n"
        F"Min Volts: \t\t{MIN_VOLTS}v\n"
        F"Alert Level: \t\t{ALERT_LEVEL:.2f}%\n"
        F"Off Level: \t\t{MIN_CAPACITY:.2f}%\n"
        F"OFF Pin: \t\t{PINS['OFF']}\n",
        flush=True
    )
    AC_OUT = GPIO.input(PINS['AC'])
    GPIO.add_event_detect(PINS['AC'], GPIO.BOTH, callback=power_changed)
    while True:
        volts = get_voltage(bus)
        capacity = get_capacity(bus)
        if DEBUG:
            print(F"\033[1A{volts:.2f} {capacity:.2f}%", flush=True)
        time.sleep(1)
        if AC_OUT:
            if(capacity <= ALERT_LEVEL or volts <= ALERT_VOLTS):
                time_left -= 1
                if PINS['BUZZ'] != 0:
                    GPIO.output(PINS['BUZZ'], 1)
                    time.sleep(.1)
                    GPIO.output(PINS['BUZZ'], 0)
            if time_left == 0 or volts < MIN_VOLTS or capacity < MIN_CAPACITY:
                call_shutdown()


if __name__ == "__main__":
    main()
