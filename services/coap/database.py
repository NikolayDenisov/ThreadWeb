import psycopg2
import config
from datetime import datetime

from table_init import query_create_db, timescale_extension_init, create_table_sensor, \
    create_table_measured_value, create_table_sensor_type, create_table_sensor_group, create_table_person, \
    create_table_alert, create_table_sensor_group_members, query_create_hypertable, query_set_timezone


def create_tables() -> None:
    with psycopg2.connect(config.Config.SQLALCHEMY_DATABASE_URI) as conn:
        cursor = conn.cursor()
        cursor.execute(create_table_sensor)
        cursor.execute(create_table_measured_value)
        cursor.execute(create_table_sensor_type)
        cursor.execute(create_table_sensor_group)
        cursor.execute(create_table_person)
        cursor.execute(create_table_alert)
        cursor.execute(create_table_sensor_group_members)
        cursor.execute(create_table_sensor_group_members)
        cursor.execute(query_create_hypertable)
        cursor.execute(query_set_timezone.format(config.Config.SQLALCHEMY_DATABASE_TIMEZONE))
        conn.commit()


def insert(query: str):
    with psycopg2.connect(config.Config.SQLALCHEMY_DATABASE_URI) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
        except Exception as error:
            print(error)
        conn.commit()


def insert_sensor(id_sensor: int, id_type: int, id_owner: int, code: int, name: int, description: str) -> None:
    sensor_insert = f'INSERT INTO \
            sensor_data(id_sensor, id_type, id_owner, code, name, description, date_created) \
            VALUES({id_sensor}, {id_type}, {id_owner}, {code}, {name}, {description}, now());'
    insert(sensor_insert)


def insert_sensor_type(name: int, unit: str, description: str) -> None:
    sensor_type_insert = f'INSERT INTO \
            sensor_typ(name, unit, description) VALUES({name}, {unit}, {description});'
    insert(sensor_type_insert)


def insert_sensor_group(id_type: int, code: str, name: str) -> None:
    sensor_group_insert = f'INSERT INTO \
            sensor_group(id_sensor, id_type, id_owner, code, name, description, date_created) \
            VALUES({id_type}, {code}, {name});'
    insert(sensor_group_insert)


def insert_sensor_group_members(group_id: int, sensor_id: int) -> None:
    sensor_group_insert = f'INSERT INTO sensor_group_members(group_id, sensor_id) \
            VALUES({group_id}, {sensor_id});'
    insert(sensor_group_insert)


def insert_person(first_name: str, last_name: str, email: str, description: str):
    person_insert = f'INSERT INTO \
            sensor_group(first_name, last_name, email, description) \
            VALUES({first_name}, {last_name}, {email}, {description});'
    insert(person_insert)


def insert_sensor_value(id_sensor: int, value: float, unit: int) -> None:
    value_insert = f'INSERT INTO \
            measured_value(id_sensor, date_measured, value, unit) \
            VALUES({id_sensor}, {value}, now() {unit});'
    insert(value_insert)


def add_sensor_group():
    pass


def add_sensor_group():
    pass


def create_db() -> None:
    with psycopg2.connect(config.Config.SQLALCHEMY_DATABASE_URI) as conn:
        cursor = conn.cursor()
        cursor.execute(query_create_db)
        cursor.execute(timescale_extension_init)
