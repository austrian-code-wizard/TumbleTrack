from twExceptions.twExceptions import *

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
        'HT1': [20, 100],   # SHT31D
    }
data_values = {
        'humidity': [20, 100],
        'temperature': [-90, 60],
        'light': [0, 427000],
        'position': [],
        'pressure': [0.19, 1.1],
        'infrared': [-20, 50],
        'air quality': [],
        'air components': []
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
data_types_range = {
        'humidity': [20, 100],
        'temperature': [-90, 60],
        'light': [0, 427000],
        'pressure': [0.19, 1.1],
        'infrared': [-20, 50],
        'air quality': [],
        'air components': []
}
data_types_actual = {
        'humidity': 0,
        'temperature': 0,
        'light': 0,
        'position': 0,
        'pressure': 0,
        'infrared': 0,
        'air quality': 0,
        'air components': 0

}

sensor_data_type = {
        'HT1': ['humidity', 'temperature'],  # SHT31D
        'IR1': ['infrared'],   # AMG8833                                Thermal Camera
        'L1': ['temperature'],  # TSL2561
        'P1': ['pressure'],  # MPL2115a2
        'D1': ['air quality'],  # PMS5003
        'C1': ['air components'],  # CCS881
        'G1': ['time', 'lon', 'lat', 'speed'],       # ultimateGPS
        'T1': ['temperature'],    # MCP9808
        'H1': ['humidity'],  # HTU21 100 foggy 20 hot summer day  in 30000 feet hight values should range between 40-50%

}
data_types_sensor = {
        'humidity': ['HT1', 'H1'],
        'temperature': ['HT1', 'T1','P1'],
        'light': ['L1'],
        'position': ['G1'],
        'pressure': ['P1'],
        'infrared': ['IR1'],
        'air quality': ['D1'],
        'air components': ['C1'],
        'altitude': ['P1'],
}
registered_sensors = []
TRESHH_DIV = 5


# https://www.goruma.de/erde-und-natur/meteorologie/luftfeuchtigkeit water/Temperature rate could be used
class sensor_test:
        """Problems:
        *How to get name of Sensor  --> Sensor check method calls new check
        *How to initialise check for all Sensors --> own class?
        *How to get all different values from same Sensor"""
        def __init__(self,sensor,name, data_type):
                self.name = name
                self.sensor = sensor
                self._add_sensor()
                self._data_types = data_type

        def _add_sensor(self):
                registered_sensors.append(self.sensor)
                if not self.name in sensor_data_type:
                            sensor_data_type[self.name] = self._data_types
                for i in range(len(self._data_types)):
                        if not self._data_types[i] in data_types_sensor:
                                data_types_sensor[self._data_types[i]] = self.name
                        else:
                                data_types_sensor[self._data_types[i]].append(self.name)


        """To be called by the sensors Check Method to import Data into the test"""
        def check_data(self, data_type, data):
                print("JOJOJ")

        """Updates the Value in the data_types_actual dict to the average of current value and new value, while checking that the new Value does not differ more than a certain 
        value from the old one."""

        def _update(self,data_type, value):
                dif = 0
                if not data_types_actual[data_type] == 0:
                        dif= abs(data_types_actual[data_type] - value)
                        deviation = data_types_range[data_type][1]-data_types_range[data_type][0]
                        deviation = (deviation*TRESHH_DIV)/100
                        if dif > deviation:
                                raise SensorInaccuracyException("Values differ more then allowed")
                        value = (max(data_types_actual[data_type], value)+ min(data_types_actual[data_type], value))/2

                data_types_actual[data_type] = value
                return dif