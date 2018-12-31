import time
from time import sleep
import random


class WaterDevice:

    def __init__(self, name, _type, brand, room, sql_controller, logger, flag):
        self.name = name
        self._type = _type
        self.brand = brand
        self.room = room
        self.sql_controller = sql_controller
        self.wd_id = None  # From data base
        self.logger = logger
        self.flag = flag

    def check_status_start(self):
        self.logger.info("Water device {} started.".format(self.name))
        while self.flag:
            value = random.randint(5, 10)
            _time = str(time.ctime())[-13:-5]
            self.logger.info("{} used {} water".format(self.name, value))
            self.sql_controller.insert_into_water_consumption(self.wd_id, value, _time)
            sleep(60)


class PowerSocket:
    """Plugged or unplugged device is not supported now"""
    def __init__(self, name, room, sql_controller, logger, flag):
        self.name = name
        self.room = room

        self.sql_controller = sql_controller
        self.ps_id = None  # From date base
        self.logger = logger
        self.flag = flag

    def check_status_start(self):
        self.logger.info("Power socket %s started.", self.name)
        while self.flag:
            value = random.randint(4, 7)
            _time = time.ctime()[-13:-5]
            self.logger.info("{} used {} power".format(self.name, value))
            self.sql_controller.insert_into_power_consumption(self.ps_id, value, _time)
            sleep(60)


class LightBulb:
    def __init__(self, name, _type, brand, room, sql_controller, logger, flag):
        self.name = name
        self._type = _type
        self.brand = brand
        self.lb_id = None  # from data base
        self.room = room
        self.sql_controller = sql_controller
        self.logger = logger
        self.flag = flag

        self.level_of_consumption = 100

    def check_status_start(self):
        self.logger.info("Light bulb started in room {}.".format(self.room.name))
        while self.flag:
            if self.level_of_consumption != 0:
                self.level_of_consumption -= 0.01
                power_consumption = random.randint(3, 6)
            else:
                self.level_of_consumption = 0
                power_consumption = 0
            _time = time.ctime()[-13:-5]
            self.logger.info(
                "Bulb {} from room {} information: level of consumption: {}, power consumption: {}.".format(
                    self.name, self.room.name, self.level_of_consumption, power_consumption))
            self.sql_controller.insert_into_light_bulb_status(self.lb_id, self.level_of_consumption,
                                                              power_consumption, _time)
            sleep(60)
