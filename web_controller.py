import logging

from interface.tools.devices_status import get_light_bulbs_status, get_power_socket_status
from interface.tools.time_converter import time_converter
from interface.tools.user_management import add_user, delete_user, get_users, login_user, change_password, get_user, \
    change_name
from simulators.enum import Rooms
import time

from flask import Flask, render_template, request, redirect

from psql.sql_controller import SqlController

app = Flask('Home controller', template_folder="interface/templates", static_folder="interface/static")
logging.basicConfig(filename='logs/home_logger.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s')

logging.basicConfig(filename='logs/interface.log', filemode='w', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s')
logger = logging.getLogger("interface_logger")
logger.info("Web server start...")

sql_controller = SqlController(logger)
sql_controller.connect()

logged = ""

@app.route("/")
def index():
    return redirect("/login", code=302)


@app.route("/home")
def home():
    if logged:
        info = {"name": logged}
        return render_template("home.html", info=info)
    else:
        info = {"log_error": ""}
        return render_template("login.html", info=info)


@app.route("/login")
def login_html():
    info = {"log_error": ""}
    return render_template("login.html", info=info)


@app.route("/log_in",  methods=['POST', 'GET'])
def login():
    global logged
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        is_ok = login_user(sql_controller, name, password)
        if is_ok:
            logged = name
            info = {"name": logged}
            return render_template("home.html", info=info)
        else:
            info = {"log_error": "Wrong name or password"}
            return render_template("login.html", info=info)


@app.route("/logout")
def logout():
    global logged
    logged = ""
    info = {"log_error": ""}
    return render_template("login.html", info=info)


@app.route("/kitchen")
def kitchen():
    if logged:
        temperature_data = sql_controller.get_temperature(Rooms.kitchen.value)
        humidity_data = sql_controller.get_humidity(Rooms.kitchen.value)
        smoke_data = sql_controller.get_smoke(Rooms.kitchen.value)
        light_bulbs_status = get_light_bulbs_status(sql_controller, Rooms.kitchen)
        power_sockets_status = get_power_socket_status(sql_controller, Rooms.kitchen)

        info = {"name": logged,
                'room_name': "Kitchen",
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
    else:
        info = {"log_error": ""}
        return render_template("login.html", info=info)


@app.route("/bathroom")
def bathroom():
    if logged:
        temperature_data = sql_controller.get_temperature(Rooms.bathroom.value)
        humidity_data = sql_controller.get_humidity(Rooms.bathroom.value)
        smoke_data = sql_controller.get_smoke(Rooms.bathroom.value)
        light_bulbs_status = get_light_bulbs_status(sql_controller, Rooms.bathroom)
        power_sockets_status = get_power_socket_status(sql_controller, Rooms.bathroom)

        info = {"name": logged,
                'room_name': "Bathroom",
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
    else:
        info = {"log_error": ""}
        return render_template("login.html", info=info)


@app.route("/bedroom")
def bedroom():
    if logged:
        temperature_data = sql_controller.get_temperature(Rooms.bedroom.value)
        humidity_data = sql_controller.get_humidity(Rooms.bedroom.value)
        smoke_data = sql_controller.get_smoke(Rooms.bedroom.value)
        light_bulbs_status = get_light_bulbs_status(sql_controller, Rooms.bedroom)
        power_sockets_status = get_power_socket_status(sql_controller, Rooms.bedroom)

        info = {"name": logged,
                'room_name': "Bedroom",
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
    else:
        info = {"log_error": ""}
        return render_template("login.html", info=info)


@app.route("/living_room")
def living_room():
    if logged:
        temperature_data = sql_controller.get_temperature(Rooms.living_room.value)
        humidity_data = sql_controller.get_humidity(Rooms.living_room.value)
        smoke_data = sql_controller.get_smoke(Rooms.living_room.value)
        light_bulbs_status = get_light_bulbs_status(sql_controller, Rooms.living_room)
        power_sockets_status = get_power_socket_status(sql_controller, Rooms.living_room)

        info = {"name": logged,
                'room_name': "Living Room",
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
    else:
        info = {"log_error": ""}
        return render_template("login.html", info=info)

@app.route("/corridor")
def corridor():
    if logged:
        temperature_data = sql_controller.get_temperature(Rooms.corridor.value)
        humidity_data = sql_controller.get_humidity(Rooms.corridor.value)
        smoke_data = sql_controller.get_smoke(Rooms.corridor.value)
        light_bulbs_status = get_light_bulbs_status(sql_controller, Rooms.corridor)
        power_sockets_status = get_power_socket_status(sql_controller, Rooms.corridor)

        info = {"name": logged,
                'room_name': "Corridor",
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
    else:
        info = {"log_error": ""}
        return render_template("login.html", info=info)


@app.errorhandler(404)
def page_404(e):
    info = {"name": logged,}
    return render_template("404.html", info=info), 404


@app.route("/users")
def users(change_password_error="", change_name_error=""):
    if logged:
        data = get_users(sql_controller)

        info = {"name": logged,
                'users': data,
                "change_password_error": change_password_error,
                "change_name_error": change_name_error}
        return render_template("users.html", info=info)
    else:
        info = {"log_error": ""}
        return render_template("login.html", info=info)


@app.route('/delete')
def user_delete():
    if logged:
        user_name = request.args.get("name")
        delete_user(sql_controller, user_name)

        return redirect("/users", code=302)
    else:
        info = {"log_error": ""}
        return render_template("login.html", info=info)


@app.route('/add_user', methods=['POST', 'GET'])
def _add_user():
    if logged:
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            add_user(sql_controller, name, password)

        return redirect("/users", code=302)
    else:
        info = {"log_error": ""}
        return render_template("login.html", info=info)


@app.route('/change_password', methods=['POST', 'GET'])
def _change_user_password():
    if logged:
        if request.method == 'POST':
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            if not get_user(sql_controller, logged)['is_admin']:
                if login_user(sql_controller, logged, old_password):
                    change_password(sql_controller, logged, new_password)
                    return redirect("/users", code=302)
                else:
                    return users(change_password_error="Wrong password")
            else:
                return users(change_password_error="Can not change Admin Password")
    else:
        info = {"log_error": ""}
        return render_template("login.html", info=info)


@app.route('/change_name', methods=['POST', 'GET'])
def _change_user_name():
    if logged:
        if request.method == 'POST':
            new_name = request.form['new_name']
            password = request.form['password_confirm']
            if not get_user(sql_controller, logged)['is_admin']:
                if login_user(sql_controller, logged, password):
                    change_name(sql_controller, logged, new_name)
                    return redirect("/users", code=302)
                else:
                    return users(change_name_error="Wrong old password")
            else:
                return users(change_name_error="Can not change Admin Name")
    else:
        info = {"log_error": ""}
        return render_template("login.html", info=info)


if __name__ == '__main__':
    app.run("0.0.0.0")
