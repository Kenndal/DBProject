import time
import threading
import numpy


class Sensor(object):
    def __init__(self, room, sql_controller, logger, flag):
        self.sql_controller = sql_controller
        self.room = room
        self.logger = logger
        self.flag = flag

    def set_flag(self, flag):
        self.flag = flag

    def start_sensor(self):
        pass


class TemperatureSensor(Sensor):

    def __init__(self, room, sql_controller, logger, flag):
        super(TemperatureSensor, self).__init__(room, sql_controller, logger, flag)

    def start_sensor(self):
        while True:
            if self.flag:
                value = numpy.random.normal(20, 3, 1)[0]
                _time = time.ctime()[-13:-5]
                temp = (value, _time)
                self.logger.info("Current temperature {} in room {}.".format(value, self.room.name))
                # TODO: add method to save random data to base
                time.sleep(60)
            else:
                return


class HumilitySensor(Sensor):

    def __init__(self, room, sql_controller, logger, flag):
        super(HumilitySensor, self).__init__(room, sql_controller, logger, flag)

    def start_sensor(self):
        while True:
            if self.flag:
                value = numpy.random.normal(60, 10, 1)[0]
                _time = time.ctime()[-13:-5]
                temp = (value, _time)
                self.logger.info("Current humidity {} in room {}.".format(value, self.room.name))
                # TODO: add method to save random data to base
                time.sleep(59)
            else:
                return


class SmokeSensor(Sensor):

    def __init__(self, room, sql_controller, logger, flag):
        super(SmokeSensor, self).__init__(room, sql_controller, logger, flag)

    def start_sensor(self):
        while True:
            if self.flag:
                value = numpy.random.normal(1, 0.2, 1)[0]
                _time = time.ctime()[-13:-5]
                temp_dict = (value, _time)
                self.logger.info("Current smoke level {} in room {}.".format(value, self.room.name))
                # TODO: add method to save random data to base
                time.sleep(61)
            else:
                return





