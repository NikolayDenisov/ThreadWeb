from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route('/sensorlog')
def sensorlog():
    query = "SELECT * FROM sensor_data;"
    with psycopg2.connect(app.config["SQLALCHEMY_DATABASE_URI"]) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        text = '<ul>'
        for row in cursor.fetchall():
            text += '<li>' + '{} {} {}'.format(row[0].strftime("%d/%m/%Y, %H:%M:%S"), row[1], row[2]) + '</li>'
        cursor.close()
        text += '</ul>'
    return text
