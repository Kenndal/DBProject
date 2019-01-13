import psycopg2
from config import config


def connect_to_db(logger, filename='psql/database.ini'):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config(filename)

        # connect to the PostgreSQL server
        logger.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        logger.info('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        logger.info(db_version)
        return conn, cur

    except (Exception, psycopg2.DatabaseError) as error:
        logger.fatal(error)


def disconnect_from_db(cursor, logger):
    try:
        logger.info("Disconnect from DB")
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.fatal(error)
