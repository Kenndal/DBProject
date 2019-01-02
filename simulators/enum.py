from aenum import Enum


class Rooms(Enum):
    """ Rooms are hardcoded, removing and adding new room is not implemented"""
    kitchen = 1
    bedroom = 2
    living_room = 3
    bathroom = 4
    corridor = 5


class SensorType(Enum):

    temperature_sensor = "temperature_sensor"
    humidity_sensor = "humidity_sensor"
    smoke_sensor = "smoke_sensor"
