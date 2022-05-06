#!/usr/bin/python

import smbus
import time

# Light level settings (lx)
LEVEL_HIGH    = 40
LEVEL_BRIGHT  = 30
LEVEL_MEDIUM  = 20
LEVEL_DARK    = 10

# Start measurement at 1 lx resolution.  Time typically 120ms.
ONE_TIME_HIGH_RES_MODE_1 = 0x20

# Start measurement at 0.5 lx resolution. Time typically 120ms.
ONE_TIME_HIGH_RES_MODE_2 = 0x21

# Default device I2C address
DEVICE = 0x23

bus = smbus.SMBus(1)

# Reads data from I2C interface
def enlighten():
    data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE_1)
    return (data[1] + (256 * data[0])) / 1.2 # convert 2 bytes into lx

# Responds to given light level
def interpret(level):
    if level > LEVEL_HIGH:
        return "too bright"
    if level > LEVEL_BRIGHT:
        return "bright"
    if level > LEVEL_MEDIUM:
        return "medium"
    if level > LEVEL_DARK:
        return "dark"
    return "too dark"

if __name__ == "__main__":
    try:
        while True:
            light = enlighten()
            sense = interpret(light)
            print("Light Level: %.2f lx - %s" % (light, sense))
            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
