timescale_extension_init = "CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;"
query_create_db = "create database example;"

query_create_sensors_table = "CREATE TABLE IF NOT EXISTS sensors (id SERIAL PRIMARY KEY," \
                             "type VARCHAR(50)," \
                             "location VARCHAR(50));"

query_create_sensordata_table = "CREATE TABLE IF NOT EXISTS sensor_data (" \
                                "time TIMESTAMPTZ NOT NULL," \
                                "sensor_id INTEGER," \
                                "temperature DOUBLE PRECISION," \
                                "FOREIGN KEY (sensor_id) REFERENCES sensors (id)" \
                                ");"

query_create_hypertable = "SELECT create_hypertable('sensor_data', 'time');"

query_change_user_password = f'ALTER USER postgres WITH PASSWORD "password";'

query_set_timezone = "SET timezone TO '{}';"
