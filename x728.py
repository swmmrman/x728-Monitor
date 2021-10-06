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
        self.PINS = {
            'AC': 6,  # AC detection pin, High when external power is lost.
            'BOOT': 12,  # Pin to signal the pi as running
            'OFF': 26,  # Pin to signal we are shutting down 26 for v2.0 and up
        }
        if(version < 2):
            self.PINS['OFF'] = 13  # 13 for older boards.

    def get_voltage(self, bus):
        address = 0x36  # Address of the Battery gauge.
        data_big_e = bus.read_word_data(address, 2)
        # Convert from big to little endian
        data_little_e = struct.unpack("<H", struct.pack(">H", data_big_e))[0]
        # convert value to Voltage, numbers from manufacturer.
        voltage = data_little_e * 1.25 / 1000 / 16
        return voltage

    def get_capacity(self, bus):
        address = 0x36  # Address of the Battery gauge.
        data_big_e = bus.read_word_data(address, 4)
        # Convert from big to little endian
        data_little_e = struct.unpack("<H", struct.pack(">H", data_big_e))[0]
        return data_little_e / 256

    def call_shutdown(self):
        GPIO.output(self.PINS['OFF'], GPIO.HIGH)  # Set shutdown pin high.
        time.sleep(4)  # 4 seconds to signal we are shutting down the X728
        GPIO.output(self.PINS['OFF'],  GPIO.LOW)  # Set back low to prevent forced off.
        print(F"{time.asctime()}:X728 Shutting down...")
        os.system('poweroff')
        # GPIO.cleanup()
        # sys.exit(0) # Exit out.