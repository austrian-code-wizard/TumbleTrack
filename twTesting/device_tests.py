from twExceptions.twExceptions import SensorConnectionException

"""Class for central Testing of the Sensor devices."""
# TODO for this class: _check_value and _check_connection except exceptions should be more specific
# [name of Sensor] : [lowest acceptable value] [highest acceptable value]
values_range = {
        'IR1': [-20, 50],   # AMG8833
        'L1': [0, 427000],  # TSL2561
        'P1': [0.19, 1.1],  # MPL2115a2
        'D1': [0, 100000],  # PMS5003 TODO get more specific value
        'C1': [0, 100000],  # CCS881  TODO get realistic values
        'G1': [0, 0],       # ultimateGPS TODO get usefull values
        'T1': [-90, 60],    # MCP9808
        'H1': [20, 100],    # HTU21 100 foggy 20 hot summer day  in 30000 feet hight values should range between 40-50%



    }
# [name of Sensor] : [manufactur ID] [device ID] [optional other registers to be checked]
values_specific = {
        'C1': [0x0054, 0x0400],  # CCS881
        'T1': [0x0054, 0x0400],  # MCP9808  (same as CCS881)
        'H1': []
}
values_specific_not = {
        'P1': [0xC4],   #MPL2115a2

}


# https://www.goruma.de/erde-und-natur/meteorologie/luftfeuchtigkeit water/Temperature rate could be used
class Device_tests:

    def __init__(self, sensor, name):
        self.check = False
        self.sensor = sensor
        self.name = name

    """Basic check to be called by every Sensors .check method."""
    def simple_check(self, *kwargs):
        correct = True
        if self.name in values_range:
            correct &= self._basic_check()
        if self.name in values_specific and len(*kwargs) > 0:
            correct &= self._check_registers(*kwargs)
        if self.name in values_specific_not and len(*kwargs) > 0:
            correct &= ~self._check_registers(*kwargs)
        return correct

    """Prints the state of a checked Sensor"""
    def print_state(self, connection, value):
        connection_message = " failed"
        value_message = " did not match or was not obtained"
        if connection:
            connection_message = " successfully"
        if value:
            value_message = " matched expected value"
        print(self.name + ": obtained value" + connection_message + ", value" + value_message)

    """Checks if values match expected Device values"""
    def _check_registers(self, *kwargs):
        correct = True
        for i in range(len(*kwargs)):
            correct &= (kwargs[i] == values_specific[self.name][i])
        return correct

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
