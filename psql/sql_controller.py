import time
from datetime import datetime

import psycopg2

from psql.connection import connect_to_db, disconnect_from_db


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
            select = self.cursor.fetchone()
            self.d_id = select[0]
            self.logger.info("Select done: " + str(select))

        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.fatal(error)

    def new_day(self):
        sql = """insert into days(date) values (%s) RETURNING d_id"""
        try:
            self.logger.info("Get new day")
            self.cursor.execute(sql, (str(datetime.now())[:9],))
            self.d_id = self.cursor.fetchone()[0]
            self.connection.commit()
            self.logger.info("New day with param: d_id:{}".format(self.d_id))
            return self.d_id
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.fatal(error)
            return None

    def insert_into_water_devices(self, water_device):
        sql = """INSERT INTO water_devices(r_id, name, type, brand) VALUES (%s, %s, %s, %s) RETURNING wd_id;"""

        try:
            self.logger.info(
                "Try to insert new Water Device {} in room {} to table water_devices...".format(water_device.name, water_device.room.name))
            self.cursor.execute(
                sql, [water_device.room.value, water_device.name, water_device._type, water_device.brand])
            wd_id = self.cursor.fetchone()[0]
            self.connection.commit()
            self.logger.info("Insert Complete. New Water Device with wd_id: {} added.".format(wd_id))
            return wd_id
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.fatal(error)
            return None

    def insert_into_water_consumption(self, wd_id, value, _time):
        sql = """insert into water_consumption(wd_id, d_id, value, time) values (%s, %s, %s, %s);"""

        try:
            self.get_day_id()
            self.logger.info("Try to insert value with params: wd_id: {} d_id: {}...".format(wd_id, self.d_id))
            self.cursor.execute(sql, (wd_id, self.d_id, value, _time))
            self.connection.commit()
            self.logger.info("Insert complete for {}.". format(wd_id))
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.fatal(error)
            return None


