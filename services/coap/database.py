import psycopg2
import config

from table_init import query_create_db, timescale_extension_init, query_create_sensors_table, \
    query_create_sensordata_table, query_create_hypertable, query_set_timezone


def create_tables():
    with psycopg2.connect(config.Config.SQLALCHEMY_DATABASE_URI) as conn:
        cursor = conn.cursor()
        cursor.execute(query_create_sensors_table)
        cursor.execute(query_create_sensordata_table)
        cursor.execute(query_create_hypertable)
        cursor.execute(query_set_timezone.format(config.Config.SQLALCHEMY_DATABASE_TIMEZONE))
        conn.commit()


def write_temp(payload):
    with psycopg2.connect(config.Config.SQLALCHEMY_DATABASE_URI) as conn:
        try:
            cursor = conn.cursor()
            sql_data_insert = "INSERT INTO sensor_data(time, sensor_id, temperature) VALUES(now(), 1, %s);"
            cursor.execute(sql_data_insert, (payload,))
        except Exception as error:
            print(error)
        conn.commit()


def create_db():
    with psycopg2.connect(config.Config.SQLALCHEMY_DATABASE_URI) as conn:
        cursor = conn.cursor()
        cursor.execute(query_create_db)
        cursor.execute(timescale_extension_init)

