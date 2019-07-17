from twExceptions.twExceptions import SensorConnectionException

"""Class for central Testing of the Sensor devices."""
# TODO for this class: _check_value and _check_connection except exceptions should be more specific
# [name of Sensor] : [lowest acceptable value] [highest acceptable value]
values_range = {
        'IR1': [-20, 50],   # AMG8833
        'L1': [0, 427000],  # TSL2561
        'P1': [0.19, 1.1],  # MPL2115a2
        'D1': [0, 100000],  # PMS5003 TODO get more specific value
        'C1': [0, 100000],  # CCS881  should have the same values as D1(PMS)
        'G1': [0, 0], # ultimateGPS TODO get usefull values
        'T1': [-90, 60],    # MCP9808
        'H1': [30, 90],       # HTU21 TODO same as PMS


    }
other_tests = {
        ''

}
# https://www.goruma.de/erde-und-natur/meteorologie/luftfeuchtigkeit water/Temperature rate could be used
class device_tests:


    def __init__(self, sensor, name):
        self.check = False
        self.sensor = sensor
        self.name = name

    """Basic check to be called by every Sensors .check method."""
    def simple_check(self):
        if self.name in values_range:
            self._basic_check()
        elif self.name in other_tests:
            print("") # TODO IMPLEMENT THIS

    """Prints the state of a checked Sensor"""
    def print_state(self, connection, value):
        connection_message = " failed"
        value_message = " did not match or was not obtained"
        if connection:
            connection_message = " successfully"
        if value:
            value_message = " matched expected value"
        print(self.name + ": obtained value" + connection_message + ", value" + value_message)

    """Checks if Values returned by get_single_measurement() match range of expectation."""
    def _check_value(self):
        try:
            value = self.sensor.get_single_measurement()
            return value > values_range[self.name][0] & value < values_range[self.name][1]
        except IOError:
            raise SensorConnectionException

    """Checks if Sensor is connected properly by trying to get measurement from Sensor."""
    def _check_connection(self):
        try:
            self.sensor.get_single_measurement()
            return True
        except IOError:
            raise SensorConnectionException

    """Checks single Sensor, basic version as used by most of our Sensors"""
    def _basic_check(self):
        value = False
        try:
            connection = self._check_connection()
            value = self._check_value()
        except SensorConnectionException:
            connection = False
        self.print_state(connection, value)
        return value & connection
