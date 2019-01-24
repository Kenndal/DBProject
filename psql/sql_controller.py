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
        self.d_id = None  # current day id.

        self.logger.info("Created psql controller.")

    def connect(self, filename='psql/database.ini'):
        self.connection, self.cursor = connect_to_db(self.logger, filename)

    def disconnect(self):
        disconnect_from_db(self.cursor, self.logger)

    def get_day_id(self):
        sql = """select * from days order by d_id;"""
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

    def get_day_date(self):
        sql = """select * from days order by d_id;"""
        try:
            self.logger.info("Try to select days")
            self.cursor.execute(sql)
            select = self.cursor.fetchall()
            self.logger.info("Select from days done: " + str(select))
            if select:
                self.connection.commit()
                return select[-1][1]
            else:
                return None

        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return None

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
            self.logger.info(
                "Try to insert value {} with params: wd_id: {} d_id: {}...".format(value, wd_id, self.d_id))
            self.cursor.execute(sql, (wd_id, self.d_id, value, _time))
            self.connection.commit()
            self.logger.info("Insert complete for wd_id: {}.".format(wd_id))
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

    def delete_device(self, name):
        """Support only water devices and light bulbs"""

        sql = ["""delete from water_devices where name = %s;""",
               """delete from light_bulbs where name = %s;"""]

        try:
            self.logger.warn("Try to delete device: {} from data base...".format(name))
            self.cursor.execute(sql[0], (name,))
            self.cursor.execute(sql[1], (name,))
            self.connection.commit()
            self.logger.warn("Deletion complete.")
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)

    def check_water_device(self, name):
        _id = None
        sql = """select wd_id from water_devices where name = %s;"""

        try:
            self.logger.info("Checking if device {} exist in database.".format(name))
            self.cursor.execute(sql, (name,))
            self.logger.info("KEK")
            _id = self.cursor.fetchone()
            self.logger.info(_id)
            self.connection.commit()
            if _id is not None:
                self.logger.info("Device {} exist in database.".format(name))
                return _id[0]
            else:
                self.logger.info("Device {} doesnt exist in database.".format(name))
                return _id
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return _id

    def check_power_socket(self, name):
        _id = None
        sql = """select ps_id from power_sockets where name = %s;"""

        try:
            self.logger.info("Checking if device {} exist in database.".format(name))
            self.cursor.execute(sql, (name,))
            _id = self.cursor.fetchone()
            self.logger.info(_id)
            self.connection.commit()
            if _id is not None:
                self.logger.info("Device {} exist in database.".format(name))
                return _id[0]
            else:
                self.logger.info("Device {} doesnt exist in database.".format(name))
                return _id
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return _id

    def check_light_bulb(self, name):
        _id = None
        sql = """select lb_id from light_bulbs where name = %s;"""
        try:
            self.logger.info("Checking if device {} exist in database.".format(name))
            self.cursor.execute(sql, (name,))
            _id = self.cursor.fetchone()
            self.logger.info(_id)
            self.connection.commit()
            if _id is not None:
                self.logger.info("Device {} exist in database.".format(name))
                return _id[0]
            else:
                self.logger.info("Device {} doesnt exist in database.".format(name))
                return _id
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return _id

    def get_bulb_level_of_consumption(self, lb_id):
        sql = """select level_of_consumption from light_bulb_status where lb_id = %s order by level_of_consumption;"""

        try:
            self.logger.info("Getting light bulb status...")
            self.cursor.execute(sql, (lb_id,))
            status = self.cursor.fetchall()[-1][0]
            self.connection.commit()
            return status
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return None

    def get_temperature(self, room_id):
        sql = """select value, time from temperature where d_id = %s and r_id = %s;"""

        try:
            self.get_day_id()
            self.logger.info("Getting data from temperature...")
            self.cursor.execute(sql, (self.d_id, room_id))
            data = self.cursor.fetchall()
            self.connection.commit()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return None

    def get_humidity(self, room_id):
        sql = """select value, time from humidity where d_id = %s and r_id = %s;"""

        try:
            self.get_day_id()
            self.logger.info("Getting data from humidity...")
            self.cursor.execute(sql, (self.d_id, room_id))
            data = self.cursor.fetchall()
            self.connection.commit()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return None

    def get_smoke(self, room_id):
        sql = """select value, time from smoke where d_id = %s and r_id = %s;"""

        try:
            self.get_day_id()
            self.logger.info("Getting data from smoke...")
            self.cursor.execute(sql, (self.d_id, room_id))
            data = self.cursor.fetchall()
            self.connection.commit()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return None

    def get_all_bulbs_from_room(self, room):
        sql = """select * from light_bulbs where r_id = %s;"""

        try:
            self.logger.info("Getting all light bulbs from room {}...".format(room.name))
            self.cursor.execute(sql, (room.value, ))
            data = self.cursor.fetchall()
            self.connection.commit()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return None

    def get_light_bulb_status(self, lb_id):
        sql = """select * from light_bulb_status where d_id = %s and lb_id = %s order by time;"""

        try:
            self.get_day_id()
            self.logger.info("Getting light bulb {} status ".format(lb_id))
            self.cursor.execute(sql, (self.d_id, lb_id))
            data = self.cursor.fetchall()
            self.logger.info(str(data))
            self.connection.commit()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return None

    def get_power_sockets_from_room(self, room):
        sql = """select * from power_sockets where r_id = %s;"""

        try:
            self.logger.info("Getting all power sockets from room {}".format(room.name))
            self.cursor.execute(sql, (room.value, ))
            data = self.cursor.fetchall()
            self.connection.commit()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return None

    def get_power_sockets_status(self, ps_id):
        sql = """select * from power_consumption where d_id =%s and ps_id = %s order by time;"""

        try:
            self.get_day_id()
            self.logger.info("Getting power socket {} consumption...".format(ps_id))
            self.cursor.execute(sql, (self.d_id, ps_id))
            data = self.cursor.fetchall()
            self.connection.commit()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return None

    def create_user(self, name, password):
        sql = """insert into users(name, password) VALUES (%s, %s);"""

        try:
            self.logger.info("Adding new user with name {}".format(name))
            self.cursor.execute(sql, (name, password))
            self.connection.commit()
            self.logger.info("Added new user with name {}".format(name))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)

    def delete_user(self, name):
        sql = """delete from users where name = %s;"""

        try:
            self.logger.info("Deleting user with name {}.".format(name))
            self.cursor.execute(sql, (name,))
            self.connection.commit()
            self.logger.info("Deleted user with name {}.".format(name))
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)

    def get_users(self):
        sql = """select name, password, is_admin from users;"""

        try:
            self.logger.info("Selecting all users.")
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            self.connection.commit()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)
            return None

    def change_password(self, name, new_password):
        sql = """update users set password = %s where name=%s;"""

        try:
            self.logger.info("Changing password...")
            self.cursor.execute(sql, (new_password, name))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)

    def change_user_name(self, old_name, new_name):
        sql = """update users set name = %s where name=%s;"""

        try:
            self.logger.info("Changing name...")
            self.cursor.execute(sql, (new_name, old_name))
            self.connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.connection.rollback()
            self.logger.fatal(error)