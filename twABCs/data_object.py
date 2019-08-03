import abc
import datetime
from dataclasses import dataclass

# TODO find types for all the dataclasses


@dataclass()
class DTO(abc):

    data: any
    created_at: datetime = datetime.datetime
    type: str = None
    id: int = None



""" 
@dataclasse
class *datatype(DTO):

    # attribute
    type: str short name for datatype
    id:  int consecutive number of measurement
    data:  data values returned by one measurement of the Sensor
    created_at: datetime time of measurement  
    next: DTO reference to next DTO object this sensor measured this "loop"
"""
if __name__ == '__main__':

    data = DTO(1.0, datetime.datetime, 'T1', 1)
    data2 = DTO.Temperature(1.0, datetime.datetime.now(), 'T1',1)


@dataclass
class Temperature(DTO):

    #attributes
    type: str = 'T'
    id: int = None
    data: float = None
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class Humidity(DTO):

    # attributes
    type: str = 'H'
    id: int = None
    data: float = None
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class Pressure(DTO):

    # attributes
    type: str = 'BP'
    id: int = None
    data: float = None
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class Lux(DTO):

    # attributes
    type: str = 'LX'
    id: int = None
    data: float = None
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class Infrared(DTO):

    # attributes
    type: str = 'IR'
    id: int = None
    data: float = None
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class Position(DTO):

    # attributes
    type: str = 'PO'
    id: int = None
    data: float = None
    created_at: datetime = datetime.datetime
    next: DTO = None

@dataclass
class Latitude(DTO):

    # attributes
    type: str = 'LA'
    id: int = None
    data: float = None
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class Quaternion(DTO):

    # attributes
    type: str = 'QI'
    id: int = None
    data: float = None  # TODO whats the datatype
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class Accelerometer(DTO):

    # attributes
    type: str = 'AC'
    id: int = None
    data: float = None
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class AccelerationLinear(DTO):

    # attributes
    type: str = 'AL'
    id: int = None
    data: float = None # TODO whats the datatype
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class Gravity(DTO):

    # attributes
    type: str = 'G'
    id: int = None
    data: float = None # TODO whats the datatype
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class Euler(DTO):

    # attributes
    type: str = 'EL'
    id: int = None
    data: float = None # TODO whats the datatype
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class Speed(DTO):
    # attributes
    type: str = 'SD'
    id: int = None
    data: float = None # TODO whats the datatype
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class Gyroscope(DTO):

    # attributes
    type: str = 'GC'
    id: int = None
    data: float() = None        # TODO whats the datatype
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class Tesla(DTO):

    # attributes
    type: str = 'MF'    # magnetic flow
    id: int = None
    data: float = None
    created_at: datetime = datetime.datetime
    next: DTO = None


@dataclass
class none(DTO):
    """ represents end of DTO list"""

'lon'
'speed'
'air quality'
'air components'

''
'quaternion'

'accelerometer'
''
