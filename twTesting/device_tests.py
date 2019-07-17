from twExceptions import *
from twExceptions.twExceptions import SensorConnectionException

"""Class for central Testing of the Sensor devices."""


class device_test:
    # [name of Sensor] : [lowest acceptable value] [highest acceptable value]
    values = {
        'IR1': [-20, 50],   # AMG8833
        'L1': [0, 427000],  # TSL2561
        'T1': [-90, 60],    # MCP9808
        'P1': [0.19, 1.1],  # MPL2115a2
        'D1': [0, 100000],  # PMS5003
    }

    def __init__(self, sensor, name):
        self.check = False
        self.sensor = sensor
        self.name = name

    """Basic check to be called by every Sensors .check method."""
    def basic_check(self):
        value = False
        try:
            connection = self.check_connection()
            value = self.check_value()
        except SensorConnectionException:
            connection = False
        self._print_state(connection,value)

    """Prints the state of a checked Sensor"""
    def _print_state(self,connection,value,**kwargs):


    """Checks if Values returned by get_single_measurement() match range of expectation."""
    def check_value(self):
        try:
            value = self.sensor.get_single_measurement()
        except #TODO find exception
            raise SensorConnectionException

    """Checks if Sensor is connected properly by trying to get measurement from Sensor."""
    def check_connection(self):
        try:
            self.sensor.get_single_measurement()
            return True
        except #TODO find exception 
            raise SensorConnectionException
