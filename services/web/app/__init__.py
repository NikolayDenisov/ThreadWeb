import psycopg2
from flask import Flask, send_from_directory, render_template
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object("app.config.Config")
cors = CORS(app, resources={r"/*": {"origins": "http://sinbiot.ru:8080"}})


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/")
def default_dashboard():
    return render_template('dashboard.html')


@app.route("/dashboard")
def user_dashboard():
    return render_template('dashboard.html')


@app.route("/devices")
def devices():
    return render_template('devices.html')


@app.route("/device-data")
def device_data():
    return render_template('device-data.html')
