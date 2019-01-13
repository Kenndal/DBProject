import logging

from interface.tools.devices_status import get_light_bulbs_status, get_power_socket_status
from interface.tools.time_converter import time_converter
from simulators.enum import Rooms
import numpy as np
import time

from flask import Flask, render_template

from psql.sql_controller import SqlController

app = Flask(__name__)
logging.basicConfig(filename='logs/home_logger.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s')
logger = logging.getLogger("interface_logger")
logger.info("Web server start...")

sql_controller = SqlController(logger)
sql_controller.connect(filename="../psql/database.ini")


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/kitchen")
def kitchen():
    temperature_data = sql_controller.get_temperature(Rooms.kitchen.value)
    humidity_data = sql_controller.get_humidity(Rooms.kitchen.value)
    smoke_data = sql_controller.get_smoke(Rooms.kitchen.value)
    light_bulbs_status = get_light_bulbs_status(sql_controller, Rooms.kitchen)
    power_sockets_status = get_power_socket_status(sql_controller, Rooms.kitchen)

    info = {'room_name': "Kitchen",
            'time': time.ctime()[-13:-5],
            # tables
            'temperature_table': [{'data': value[0], 'time': value[1]} for value in temperature_data[-4:]],
            'humidity_table': [{'data': value[0], 'time': value[1]} for value in humidity_data[-4:]],
            'smoke_table': [{'data': value[0], 'time': value[1]} for value in smoke_data[-4:]],
            'light_bulbs_status': light_bulbs_status,
            'power_sockets_status': power_sockets_status,
            # temperature chart
            'temperature_data': [value[0] for value in temperature_data],
            'temperature_time': [time_converter(value[1]) for value in temperature_data],
            # humidity chart
            'humidity_data': [value[0] for value in humidity_data],
            'humidity_time': [time_converter(value[1]) for value in humidity_data],
            # smoke chart
            'smoke_data': [value[0] for value in smoke_data],
            'smoke_time': [time_converter(value[1]) for value in smoke_data]}

    return render_template("room_information.html", info=info)


@app.route("/bathroom")
def bathroom():
    temperature_data = sql_controller.get_temperature(Rooms.bathroom.value)
    humidity_data = sql_controller.get_humidity(Rooms.bathroom.value)
    smoke_data = sql_controller.get_smoke(Rooms.bathroom.value)
    light_bulbs_status = get_light_bulbs_status(sql_controller, Rooms.bathroom)
    power_sockets_status = get_power_socket_status(sql_controller, Rooms.bathroom)

    info = {'room_name': "Bathroom",
            'time': time.ctime()[-13:-5],
            # tables
            'temperature_table': [{'data': value[0], 'time': value[1]} for value in temperature_data[-4:]],
            'humidity_table': [{'data': value[0], 'time': value[1]} for value in humidity_data[-4:]],
            'smoke_table': [{'data': value[0], 'time': value[1]} for value in smoke_data[-4:]],
            'light_bulbs_status': light_bulbs_status,
            'power_sockets_status': power_sockets_status,
            # temperature chart
            'temperature_data': [value[0] for value in temperature_data],
            'temperature_time': [time_converter(value[1]) for value in temperature_data],
            # humidity chart
            'humidity_data': [value[0] for value in humidity_data],
            'humidity_time': [time_converter(value[1]) for value in humidity_data],
            # smoke chart
            'smoke_data': [value[0] for value in smoke_data],
            'smoke_time': [time_converter(value[1]) for value in smoke_data]}

    return render_template("room_information.html", info=info)


@app.route("/bedroom")
def bedroom():
    temperature_data = sql_controller.get_temperature(Rooms.bedroom.value)
    humidity_data = sql_controller.get_humidity(Rooms.bedroom.value)
    smoke_data = sql_controller.get_smoke(Rooms.bedroom.value)
    light_bulbs_status = get_light_bulbs_status(sql_controller, Rooms.bedroom)
    power_sockets_status = get_power_socket_status(sql_controller, Rooms.bedroom)

    info = {'room_name': "Bedroom",
            'time': time.ctime()[-13:-5],
            # tables
            'temperature_table': [{'data': value[0], 'time': value[1]} for value in temperature_data[-4:]],
            'humidity_table': [{'data': value[0], 'time': value[1]} for value in humidity_data[-4:]],
            'smoke_table': [{'data': value[0], 'time': value[1]} for value in smoke_data[-4:]],
            'light_bulbs_status': light_bulbs_status,
            'power_sockets_status': power_sockets_status,
            # temperature chart
            'temperature_data': [value[0] for value in temperature_data],
            'temperature_time': [time_converter(value[1]) for value in temperature_data],
            # humidity chart
            'humidity_data': [value[0] for value in humidity_data],
            'humidity_time': [time_converter(value[1]) for value in humidity_data],
            # smoke chart
            'smoke_data': [value[0] for value in smoke_data],
            'smoke_time': [time_converter(value[1]) for value in smoke_data]}

    return render_template("room_information.html", info=info)


@app.route("/living_room")
def living_room():
    temperature_data = sql_controller.get_temperature(Rooms.living_room.value)
    humidity_data = sql_controller.get_humidity(Rooms.living_room.value)
    smoke_data = sql_controller.get_smoke(Rooms.living_room.value)
    light_bulbs_status = get_light_bulbs_status(sql_controller, Rooms.living_room)
    power_sockets_status = get_power_socket_status(sql_controller, Rooms.living_room)

    info = {'room_name': "Living Room",
            'time': time.ctime()[-13:-5],
            # tables
            'temperature_table': [{'data': value[0], 'time': value[1]} for value in temperature_data[-4:]],
            'humidity_table': [{'data': value[0], 'time': value[1]} for value in humidity_data[-4:]],
            'smoke_table': [{'data': value[0], 'time': value[1]} for value in smoke_data[-4:]],
            'light_bulbs_status': light_bulbs_status,
            'power_sockets_status': power_sockets_status,
            # temperature chart
            'temperature_data': [value[0] for value in temperature_data],
            'temperature_time': [time_converter(value[1]) for value in temperature_data],
            # humidity chart
            'humidity_data': [value[0] for value in humidity_data],
            'humidity_time': [time_converter(value[1]) for value in humidity_data],
            # smoke chart
            'smoke_data': [value[0] for value in smoke_data],
            'smoke_time': [time_converter(value[1]) for value in smoke_data]}

    return render_template("room_information.html", info=info)


@app.route("/corridor")
def corridor():
    temperature_data = sql_controller.get_temperature(Rooms.corridor.value)
    humidity_data = sql_controller.get_humidity(Rooms.corridor.value)
    smoke_data = sql_controller.get_smoke(Rooms.corridor.value)
    light_bulbs_status = get_light_bulbs_status(sql_controller, Rooms.corridor)
    power_sockets_status = get_power_socket_status(sql_controller, Rooms.corridor)

    info = {'room_name': "Corridor",
            'time': time.ctime()[-13:-5],
            # tables
            'temperature_table': [{'data': value[0], 'time': value[1]} for value in temperature_data[-4:]],
            'humidity_table': [{'data': value[0], 'time': value[1]} for value in humidity_data[-4:]],
            'smoke_table': [{'data': value[0], 'time': value[1]} for value in smoke_data[-4:]],
            'light_bulbs_status': light_bulbs_status,
            'power_sockets_status': power_sockets_status,
            # temperature chart
            'temperature_data': [value[0] for value in temperature_data],
            'temperature_time': [time_converter(value[1]) for value in temperature_data],
            # humidity chart
            'humidity_data': [value[0] for value in humidity_data],
            'humidity_time': [time_converter(value[1]) for value in humidity_data],
            # smoke chart
            'smoke_data': [value[0] for value in smoke_data],
            'smoke_time': [time_converter(value[1]) for value in smoke_data]}

    return render_template("room_information.html", info=info)


@app.errorhandler(404)
def page_404(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
