timescale_extension_init = "CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;"
query_create_db = "create database example;"

query_create_sensors_table = "CREATE TABLE IF NOT EXISTS sensors (id SERIAL PRIMARY KEY," \
                             "type VARCHAR(50)," \
                             "location VARCHAR(50));"

query_create_sensordata_table = "CREATE TABLE IF NOT EXISTS sensor_data (" \
                                "time TIMESTAMPTZ NOT NULL," \
                                "sensor_id INTEGER," \
                                "eui64 VARCHAR(50)," \
                                "temperature DOUBLE PRECISION," \
                                "FOREIGN KEY (sensor_id) REFERENCES sensors (id)" \
                                ");"
#TODO.md Добавить группы сенсоров
#TODO.md Добавить sensor_owner
#TODO.md Добавить единицу измерения
'''
Sensors
    sensor_id - уникальный id сенсора
    service_date - когда добавили сенсор
    sensor_model - модель сенсор (nrf52840)
    sensor_manufacturer - производитель
    sensor_owner - кто добавил сенсор
    location - где установлен датчик
    time - время добавления сенсора

Sensor_data
    sensor_id
    time - время добавления данных
    unit - тип измерения(температура, влажность, напряжение)
    value - данные замера
Группы сенсоро
    id
    group_name
'''

query_create_devices_table = "CREATE TABLE IF NOT EXISTS devices (" \
                             "id SERIAL PRIMARY KEY," \
                             "type_id INTEGER," \
                             "owner_id INTEGER," \
                             "created_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP," \
                             "FOREIGN KEY (type_id) REFERENCES device_type(id)," \
                             "FOREIGN KEY(owner_id) REFERENCES users(id)," \
                             "eui64 VARCHAR(50)," \
                             "location VARCHAR(50));"

query_create_device_type_table = "CREATE TABLE IF NOT EXISTS device_type (" \
                             "id SERIAL PRIMARY KEY," \
                             "vendor VARCHAR(50)," \
                             "model VARCHAR(50));"

query_create_device_data_table = "CREATE TABLE IF NOT EXISTS device_data (" \
                                "created_date TIMESTAMPTZ NOT NULL," \
                                "device_id INTEGER," \
                                "FOREIGN KEY(device_id) REFERENCES devices(id)," \
                                "value DOUBLE PRECISION," \
                                "unit INTEGER" \
                                ");"

query_create_device_group_table = "CREATE TABLE IF NOT EXISTS device_group (" \
                                  "id SERIAL PRIMARY KEY," \
                                  "code VARCHAR(20)," \
                                  "group_name VARCHAR(50)" \
                                  ");"

query_create_device_group_members_table = "CREATE TABLE IF NOT EXISTS device_group_members (" \
                                  "id SERIAL PRIMARY KEY," \
                                  "group_id INTEGER," \
                                  "device_id INTEGER," \
                                  "FOREIGN KEY(group_id) REFERENCES device_group(id)," \
                                  "FOREIGN KEY(device_id) REFERENCES devices(id)" \
                                  ");"

query_create_hypertable = "SELECT create_hypertable('device_data', 'time');"

query_change_user_password = f'ALTER USER postgres WITH PASSWORD "password";'

query_set_timezone = "SET timezone TO '{}';"
