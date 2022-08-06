import psycopg2
from flask import Flask, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy

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
    eui64 = 'F4:CE:36:86:38:EC'
    data = last_day(eui64)
    timestamps = list(list(zip(*data))[0])
    date_strings = [d.strftime('%d/%m/%Y, %H:%M:%S') for d in timestamps]
    temps = list(list(zip(*data))[1])
    return render_template('chart.html', values=temps, labels=date_strings)


@app.route("/dashboard")
def dashboard():
    eui64 = 'F4:CE:36:86:38:EC'
    data = last_day(eui64)
    timestamps = list(list(zip(*data))[0])
    date_strings = [d.strftime('%d/%m/%Y, %H:%M:%S') for d in timestamps]
    temps = list(list(zip(*data))[1])
    return render_template('dashboard.html', values=temps, labels=date_strings)


@app.route("/devices")
def devices():
    query = "SELECT * FROM sensor_data;"
    return render_template('devices.html')


def connect(query: str):
    with psycopg2.connect(app.config["SQLALCHEMY_DATABASE_URI"]) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
    return data


@app.route("/device-data")
def device_data():
    query = "SELECT * FROM sensor_data;"
    data = connect(query)
    return render_template('device-data.html')


def last_day(eui64):
    query = "SELECT time_bucket('1 hours', time) AS one_hour," \
            "ROUND(AVG(temperature)::numeric, 2) FROM sensor_data " \
            "WHERE time > now () - INTERVAL '1 day' AND " \
            f"eui64='{eui64}'" \
            "GROUP BY one_hour ORDER BY one_hour;"
    data = connect(query)
    return data


class Sensor:
    def __init__(self, eui64):
        self.eu64 = eui64

    def get_eui64(self):
        return self.eu64

    def read_value(self):
        pass

    def write_value(self):
        pass
