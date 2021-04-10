#!/usr/bin/env python3

import smbus
import time
import x728

bus = smbus.SMBus(1)
x728.get_voltage(bus)
