from twExceptions.twExceptions import SensorConnectionException

"""Class for central Testing of the Sensor devices."""
# TODO for this class: check_value and check_connection except exceptions should be more specific
values = {
        'IR1': [-20, 50],   # AMG8833
        'L1': [0, 427000],  # TSL2561
        'T1': [-90, 60],    # MCP9808
        'P1': [0.19, 1.1],  # MPL2115a2
        'D1': [0, 100000],  # PMS5003
    }


class device_tests:
    # [name of Sensor] : [lowest acceptable value] [highest acceptable value]

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
        self.print_state(connection, value)

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
    def check_value(self):
        try:
            value = self.sensor.get_single_measurement()
            return value > values[self.name][0] & value < values[self.name][1]
        except IOError:
            raise SensorConnectionException

    """Checks if Sensor is connected properly by trying to get measurement from Sensor."""
    def check_connection(self):
        try:
            self.sensor.get_single_measurement()
            return True
        except IOError:
            raise SensorConnectionException
