from twExceptions.twExceptions import *
from twDevices.mcp9808 import MCP9808

"""Class for central Testing of the Sensor devices."""

# [name of Sensor] : [manufactur ID] [device ID] [optional other registers to be checked]
reg_values_specific = {
        'C1': {MCP9808.MCP9808_REG_MANUF_ID: 0x0054,
               MCP9808.MCP9808_REG_DEVICE_ID: 0x0400},  # CCS881
        'T1': {MCP9808.MCP9808_REG_MANUF_ID: 0x0054,
               MCP9808.MCP9808_REG_DEVICE_ID: 0x0400},  # TODO somehow reverence to 'C1'
        'H1': []
}
values_specific_not = {
        'P1': { 0xC4},
}
data_types_range = {
        'humidity': [20, 100],
        'temperature': [-90, 60],
        'light': [0, 427000],
        'pressure': [0.19, 1.1],
        'infrared': [-20, 50],
        'air quality': [],
        'air components': [],
        'position': [],
}
data_types_actual = {
}

registered_sensors = []
TRESHH_DIV = 5


# https://www.goruma.de/erde-und-natur/meteorologie/luftfeuchtigkeit water/Temperature rate could be used
class sensor_test:

        def __init__(self, sensor, name):
                self._sensor = sensor
                self._name = name

        """Tests data of Sensor against data of other Sensors if available"""
        def test_data(self, data_type, data):
                if data_type not in data_types_range:
                        raise TypeError("Invalid Data Type")
                else:
                        limits = data_types_range[data_type]
                        if not data > limits[0] & data < limits[1]:
                                return False
                if data_type in data_types_actual:
                        per = (limits[1] - limits[0])/100
                        dif = abs(data - data_types_actual[data_type])
                        bol = (per*TRESHH_DIV) >= dif
                        if bol:
                                data_types_actual[data_type] = (data + data_types_actual[data_type])/2
                        return bol
                else:
                        data_types_actual[data_type] = data

                return True

        """"""
        def test_register(self, value, register, equals = True):
                 print("Implement this")