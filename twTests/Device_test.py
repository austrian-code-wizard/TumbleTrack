from twDevices import *


class test():
    # [name of Sensor] : [lowest acceptable value] [highest acceptable value]
    values = {
        'IR1': [-20, 50],   # AMG8833
        'L1': [0, 427000],  # TSL2561
        'T1': [-90, 60],    # MCP9808
        'P1': [0.19, 1.1],  # MPL2115a2
        'D1': [0, 100000],         # PMS5003
    }

    def __init__(self, sensor, name):
        self.check = False
        self.sensor = sensor
        self.name = name

    def check_value(self, value, alt_value = None):
        return

    def check_connection(self):
        try:
            self.sensor.get_single_measurement()
        except IOError:
            print("Testing Sensor "+ self.name + "failed: ")
            print("could not measure value")
        return False
