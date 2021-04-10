#!/usr/bin/env python3

import smbus
import time
import x728

bus = smbus.SMBus(1)
voltage = x728.get_voltage(bus)
capacity = x728.get_capacity(bus)
print(
        F"<-----Current Status----->\n"
        F"\tVoltage: {voltage:.2f}v\n"
        F"\tCapacity: {capacity:.2f}%\n"
      ),
