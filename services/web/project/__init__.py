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
    password = db.Column(db.String(255), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, email):
        self.email = email


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class Organization:
    id = ''
    name = ''


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
    query = "SELECT devices.id, device_type.vendor, devices.created_date, devices.eui64, devices.location  " \
            "FROM devices " \
            "INNER JOIN device_type ON devices.type_id = device_type.id;"
    data = connect(query)
    print(data)
    return render_template('devices.html', data=data)


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
