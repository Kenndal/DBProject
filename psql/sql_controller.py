import psycopg2

from psql.connection import connect_to_db, disconnect_from_db
from simulators.enum import Rooms


class SqlController:
    def __init__(self, logger):
        self.logger = logger
        self.cursor = None
        self.connection = None

        self.logger.info("Created sql controller.")

    def connect(self):
        self.connection, self.cursor = connect_to_db(self.logger)

    def disconnect(self):
        disconnect_from_db(self.cursor, self.logger)

    def insert_into_water_devices(self, water_device):
        sql = """INSERT INTO water_devices(r_id, name, type, brand) VALUES (%s, %s, %s, %s) RETURNING wd_id;"""

        try:
            self.logger.info(
                "Try to insert new Water Device {} in room {}...".format(water_device.name, water_device.room.name))
            self.cursor.execute(
                sql, [water_device.room.value, water_device.name, water_device._type, water_device.brand])
            wd_id = self.cursor.fetchone()[0]
            self.connection.commit()
            self.logger.info("Insert Complete. New Water Device with wd_id: {} added.".format(wd_id))
            return wd_id
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.fatal(error)
            return None




