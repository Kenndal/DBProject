import time
from datetime import datetime

import psycopg2

from psql.connection import connect_to_db, disconnect_from_db
from simulators.enum import SensorType


class SqlController:
    def __init__(self, logger):
        self.logger = logger
        self.cursor = None
        self.connection = None
        self.d_id = None

        self.logger.info("Created psql controller.")

    def connect(self):
        self.connection, self.cursor = connect_to_db(self.logger)

    def disconnect(self):
        disconnect_from_db(self.cursor, self.logger)

    def get_day_id(self):
        sql = """select * from days;"""
        try:
            self.logger.info("Try to select days")
            self.cursor.execute(sql)
            select = self.cursor.fetchall()[-1]
            self.d_id = select[0]
            self.logger.info("Select from days done: " + str(select))
            self.connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)

    def new_day(self):
        sql = """insert into days(date) values (%s) RETURNING d_id"""
        try:
            self.logger.info("Get new day")
            self.cursor.execute(sql, (str(datetime.now())[:10],))
            self.d_id = self.cursor.fetchone()[0]
            self.connection.commit()
            self.logger.info("New day with param: d_id:{}".format(self.d_id))
            return self.d_id
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.fatal(error)
            self.connection.rollback()
            return None

    def insert_into_water_devices(self, water_device):
        sql = """INSERT INTO water_devices(r_id, name, type, brand) VALUES (%s, %s, %s, %s) RETURNING wd_id;"""

        try:
            self.logger.info(
                "Try to insert new Water Device {} in room {} to table water_devices...".format(water_device.name,
                                                                                                water_device.room.name))
            self.cursor.execute(
                sql, [water_device.room.value, water_device.name, water_device._type, water_device.brand])
            wd_id = self.cursor.fetchone()[0]
            self.connection.commit()
            self.logger.info("Insert Complete. New Water Device with wd_id: {} added.".format(wd_id))
            return wd_id
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.fatal(error)
            self.connection.rollback()
            return None

    def insert_into_water_consumption(self, wd_id, value, _time):
        sql = """insert into water_consumption(wd_id, d_id, value, time) values (%s, %s, %s, %s);"""

        try:
            self.get_day_id()
            self.logger.info("Try to insert value {} with params: wd_id: {} d_id: {}...".format(value, wd_id, self.d_id))
            self.cursor.execute(sql, (wd_id, self.d_id, value, _time))
            self.connection.commit()
            self.logger.info("Insert complete for wd_id: {}.". format(wd_id))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)

    def insert_into_power_sockets(self, power_socket):
        sql = "insert into power_sockets (r_id, name) values (%s, %s) returning ps_id;"

        try:
            self.logger.info(
                "Try to insert new Power Socket {} in room {} to table power_sockets...".format(power_socket.name,
                                                                                                power_socket.room.name))
            self.cursor.execute(sql, (power_socket.room.value, power_socket.name))
            ps_id = self.cursor.fetchone()[0]
            self.connection.commit()
            self.logger.info("Insert Complete. New Power Socket with ps_is: {} added.".format(ps_id))
            return ps_id
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return None

    def insert_into_power_consumption(self, ps_id, value, _time):
        sql = """insert into power_consumption (ps_id, d_id, value, time) values (%s, %s, %s, %s);"""

        try:
            self.get_day_id()
            self.logger.info("Try to insert value {} with params: ps_id: {}, d_id: {}.".format(value, ps_id, self.d_id))
            self.cursor.execute(sql, (ps_id, self.d_id, value, _time))
            self.connection.commit()
            self.logger.info("Insert complete for ps_id: {}".format(ps_id))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)

    def insert_into_light_bulbs(self, light_bulb):
        sql = """insert into light_bulbs (r_id, name, type, brand) values (%s, %s, %s, %s) returning lb_id"""

        try:
            self.logger.info(
                "Try to insert new Light Bulb in room {} to table light_bulbs...".format(light_bulb.room.name))
            self.cursor.execute(sql, (light_bulb.room.value, light_bulb.name, light_bulb._type, light_bulb.brand))
            lb_id = self.cursor.fetchone()[0]
            self.connection.commit()
            self.logger.info("Insert Complete. New Light Bulb with lb_id: {} added.".format(lb_id))
            return lb_id
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return None

    def insert_into_light_bulb_status(self, lb_id, level_of_consumption, power_consumption, _time):
        sql = """insert into light_bulb_status (lb_id, d_id, level_of_consumption, power_consumption, time)
         values (%s, %s, %s, %s, %s);"""

        try:
            self.get_day_id()
            self.logger.info("Try to insert values: {}, {} with params: lb_id: {}, d_id: {}.".format(
                level_of_consumption, power_consumption, lb_id, self.d_id))

            self.cursor.execute(sql, (lb_id, self.d_id, level_of_consumption, power_consumption, _time))
            self.connection.commit()
            self.logger.info("Insert complete for lb_id: {}.".format(lb_id))

        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)

    def insert_into_sensor_table(self, room, value, _time, sensor_type):
        if sensor_type == SensorType.temperature_sensor:
            sql = """insert into temperature (r_id, d_id, time, value) values (%s, %s, %s, %s);"""
        elif sensor_type == SensorType.humidity_sensor:
            sql = """insert into humidity (r_id, d_id, time, value) values (%s, %s, %s, %s);"""
        elif sensor_type == SensorType.smoke_sensor:
            sql = """insert into smoke (r_id, d_id, time, value) values (%s, %s, %s, %s);"""
        else:
            raise ValueError("Wrong sensor type, sensor not created.")

        try:
            self.get_day_id()
            self.logger.info("Try to insert value: {} from sensor: {} in room: {}...".format(value, sensor_type.name,
                                                                                          room.name))
            self.cursor.execute(sql, (room.value, self.d_id, _time, value))
            self.connection.commit()
            self.logger.info("Insert complete for sensor {}".format(sensor_type.name))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
