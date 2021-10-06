import os
import struct
import time
import RPi.GPIO as GPIO

if __name__ == "__main__":
    print("I cannot be run directly")


class x728(object):
    """x728 controller."""

    def __init__(self, version, bus):
        self.version = version
        self.bus = bus
        self.PINS = {
            'AC': 6,  # AC detection pin, High when external power is lost.
            'BOOT': 12,  # Pin to signal the pi as running
            'OFF': 26,  # Pin to signal we are shutting down 26 for v2.0 and up
        }
        if(version < 2):
            self.PINS['OFF'] = 13  # 13 for older boards.
        self.voltage = self.get_voltage()
        self.capacity = self.capacity()
        self.ac_status = GPIO.input(self.PINS['AC'])

    def endian_swap(value):
        """Convert from big to little endian"""
        return struct.unpack("<H", struct.pack(">H", value))[0]

    def get_voltage(self):
        """Fetch the current voltage of the batteries"""
        address = 0x36  # Address of the Battery gauge.
        data = self.endian_swap(self.bus.read_word_data(address, 2))
        # convert value to Voltage, numbers from manufacturer.
        voltage = data * 1.25 / 1000 / 16
        return voltage

    def get_capacity(self):
        """Fetch the current capacity from the device"""
        address = 0x36  # Address of the Battery gauge.
        data = self.endian_swap(self.bus.read_word_data(address, 4))
        # convert to capacity and return
        return data / 256

    def call_shutdown(self):
        """
        Shutdown x728
        Steps for shutdown
        Set off pin high for 4 second, then back low. 6 seconds is forced off.
        Send log message and call poweroff.
        """
        GPIO.output(self.PINS['OFF'], GPIO.HIGH)
        time.sleep(4)
        GPIO.output(self.PINS['OFF'],  GPIO.LOW)
        print(F"{time.asctime()}:X728 Shutting down...")
        os.system('poweroff')
