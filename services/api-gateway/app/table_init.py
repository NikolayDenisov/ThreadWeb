commands = []

timescale_extension_init = "CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;"
query_create_db = "create database example;"

create_table_sensor = "CREATE TABLE IF NOT EXISTS sensor (" \
                      "id SERIAL PRIMARY KEY," \
                      "id_type INTEGER references sensor_type(id)," \
                      "id_owner INTEGER references person(id)," \
                      "code VARCHAR(20) UNIQUE," \
                      "name VARCHAR(50)," \
                      "description VARCHAR(80)," \
                      "date_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP" \
                      ");"

create_table_sensor_type = "CREATE TABLE IF NOT EXISTS sensor_type (" \
                           "id SERIAL PRIMARY KEY," \
                           "name VARCHAR(30)," \
                           "unit VARCHAR(15)," \
                           "description VARCHAR(160)" \
                           ");"

create_table_sensor_group = "CREATE TABLE IF NOT EXISTS sensor_group (" \
                            "id SERIAL PRIMARY KEY," \
                            "id_type INTEGER references sensor_type(id)," \
                            "code VARCHAR(20) UNIQUE," \
                            "name VARCHAR(50)" \
                            ");"

create_table_sensor_group_members = "CREATE TABLE IF NOT EXISTS sensor_group_members (" \
                                    "id SERIAL PRIMARY KEY," \
                                    "group_id INTEGER REFERENCES sensor_group(id)," \
                                    "sensor_id INTEGER REFERENCES sensor(id)" \
                                    ");"

create_table_measured_value = "CREATE TABLE IF NOT EXISTS measured_value (" \
                              "id SERIAL PRIMARY KEY," \
                              "id_sensor INTEGER REFERENCES sensor(id)," \
                              "date_measured TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP," \
                              "value DOUBLE PRECISION," \
                              "unit VARCHAR(30)" \
                              ");"

create_table_person = "CREATE TABLE IF NOT EXISTS person (" \
                      "id SERIAL PRIMARY KEY," \
                      "first_name VARCHAR(20)," \
                      "last_name VARCHAR(20)," \
                      "email VARCHAR(30)," \
                      "description VARCHAR(80)" \
                      ");"

create_table_alert = "CREATE TABLE IF NOT EXISTS alert (" \
                     "id SERIAL PRIMARY KEY," \
                     "id_sensor INTEGER REFERENCES sensor(id)," \
                     "threshold DOUBLE PRECISION," \
                     "active BOOLEAN NOT NULL," \
                     "alert_mode varchar(8)," \
                     "mail_recipient VARCHAR(30)," \
                     "mail_subject VARCHAR(50)" \
                     ");"

query_create_hypertable = "SELECT create_hypertable('measured_value', 'date_measured');"

query_change_user_password = "ALTER USER postgres WITH PASSWORD 'password';"

query_set_timezone = "SET timezone TO 'Asia/Yekaterinburg';"

commands.append(query_change_user_password)
commands.append(timescale_extension_init)
commands.append(query_create_db)
commands.append(query_create_hypertable)
commands.append(query_set_timezone)
commands.append(create_table_sensor_type)
commands.append(create_table_person)
commands.append(create_table_sensor)
commands.append(create_table_sensor_group)
commands.append(create_table_sensor_group_members)
commands.append(create_table_alert)
commands.append(create_table_measured_value)
