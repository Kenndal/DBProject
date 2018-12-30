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
        self.logger.info("Water devise {} started.".format(self.name))
        while self.flag:
            value = random.randint(5, 10)
            self.logger.info("{} used {} water".format(self.name, value))
            # TODO add method to save value in database (TABLE Water Consumption)
            sleep(20)


class PowerSocket:

    def __init__(self, name, room, sql_controller, logger, flag):
        self.name = name
        self.room = room

        self.sql_controller = sql_controller
        self.ps_id = None  # From date base
        self.logger = logger
        self.flag = flag
        # TODO: Add method which add new device to base (TABLE Power Sockets) Return ps_id.

    def check_status_start(self):
        self.logger.info("Power socket %s started.", self.name)
        while self.flag:
            value = random.randint(4, 7)
            self.logger.info("{} used {} power".format(self.name, value))
            # TODO add method to save value in database (TABLE Power Consumption)
            sleep(3600)


class LightBulb:
    def __init__(self, _type, brand, room, sql_controller, logger, flag):
        self._type = _type
        self.brand = brand
        self.lb_id = None  # from data base
        self.room = room
        self.sql_controller = sql_controller
        self.logger = logger
        self.flag = flag

        self.level_of_consumption = 100
        # TODO: Add method which add new device to base (TABLE Light Bulbs) Return ps_id.

    def check_status_start(self):
        self.logger.info("Light bulb started in room {}.".format(self.room.name))
        while self.flag:
            self.level_of_consumption -= 0.01
            if self.level_of_consumption != 0:
                power_consumption = random.randint(3, 6)
            else:
                power_consumption = 0
            self.logger.info(
                "Bulb from room %{} information: level of consumption: {}, power consumption: {}.".format(
                    self.room.name, self.level_of_consumption, power_consumption))
            # TODO add method to save value in database (TABLE Light bulbs status)
            sleep(3600)
