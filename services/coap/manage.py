from flask.cli import FlaskGroup
from flask import Flask

import psycopg2

app = Flask(__name__)
app.config.from_object("config.Config")
cli = FlaskGroup(app)


def create_db():
    conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    cursor = conn.cursor()
    query_create_sensors_table = "CREATE TABLE sensors (id SERIAL PRIMARY KEY, type VARCHAR(50), location VARCHAR(50));"
    cursor.execute(query_create_sensors_table)
    conn.commit()
    cursor.close()


if __name__ == "__main__":
    create_db()