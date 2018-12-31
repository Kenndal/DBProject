import time
import threading
import numpy


class Sensor(object):
    def __init__(self, room, sql_controller, logger, sensor_type, flag):
        self.sql_controller = sql_controller
        self.room = room
        self.logger = logger
        self.sensor_type = sensor_type
        self.flag = flag

    def set_flag(self, flag):
        self.flag = flag

    def start_sensor(self):
        pass


class TemperatureSensor(Sensor):

    def __init__(self, room, sql_controller, logger, sensor_type, flag):
        super(TemperatureSensor, self).__init__(room, sql_controller, logger, sensor_type, flag)

    def start_sensor(self):
        while True:
            if self.flag:
                value = numpy.random.normal(20, 3, 1)[0]
                _time = time.ctime()[-13:-5]
                self.logger.info("Current temperature {} in room {}.".format(value, self.room.name))
                self.sql_controller.insert_into_sensor_table(self.room, value, _time, self.sensor_type)
                time.sleep(30)
            else:
                return


class HumilitySensor(Sensor):

    def __init__(self, room, sql_controller, logger, sensor_type, flag):
        super(HumilitySensor, self).__init__(room, sql_controller, logger, sensor_type, flag)

    def start_sensor(self):
        while True:
            if self.flag:
                value = numpy.random.normal(60, 10, 1)[0]
                _time = time.ctime()[-13:-5]
                self.logger.info("Current humidity {} in room {}.".format(value, self.room.name))
                self.sql_controller.insert_into_sensor_table(self.room, value, _time, self.sensor_type)
                time.sleep(30)
            else:
                return


class SmokeSensor(Sensor):

    def __init__(self, room, sql_controller, logger, sensor_type, flag):
        super(SmokeSensor, self).__init__(room, sql_controller, logger, sensor_type, flag)

    def start_sensor(self):
        while True:
            if self.flag:
                value = numpy.random.normal(1, 0.2, 1)[0]
                _time = time.ctime()[-13:-5]
                self.logger.info("Current smoke level {} in room {}.".format(value, self.room.name))
                self.sql_controller.insert_into_sensor_table(self.room, value, _time, self.sensor_type)
                time.sleep(30)
            else:
                return





