import psycopg2
from flask import Flask, send_from_directory, render_template

app = Flask(__name__)
app.config.from_object("app.config.Config")


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
