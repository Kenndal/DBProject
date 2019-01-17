import threading
from time import sleep

from psql.sql_controller import SqlController
from simulators.day import Day
from simulators.devices import WaterDevice, PowerSocket, LightBulb
import logging
from simulators.enum import SensorType, Rooms
from simulators.sensors import TemperatureSensor, HumilitySensor, SmokeSensor


class HomeController:

    def __init__(self):
        # Create logger
        logging.basicConfig(filename='logs/home_logger.log', filemode='w', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s')
        self.logger = logging.getLogger("home_logger")
        self.logger.info("Home Controller started.")

        # Create psql controller
        self.sql_controller = SqlController(self.logger)
        self.sql_controller.connect()

        self.sensor_list = []
        self.device_list = []
        self.device_thread_list = []
        self.sensor_thread_list = []
        self.flag = True

        self.day = Day(self.sql_controller, self.logger, self.flag)
        self.day_thread = threading.Thread(target=self.day.start)
        self.day_thread.start()

        self.check_thread = None

    def add_water_device(self, name, _type, brand, room):
        self.logger.info("Create water device with name {}.".format(name))
        water_device = WaterDevice(name, _type, brand, room, self.sql_controller, self.logger, self.flag)
        wd_id = self.sql_controller.check_water_device(name)
        if wd_id is None:
            wd_id = self.sql_controller.insert_into_water_devices(water_device)
            if wd_id is not None:
                water_device.wd_id = wd_id
                self.device_list.append(water_device)
            else:
                self.logger.warn("Removing {}".format(water_device.name))
                del water_device
        else:
            water_device.wd_id = wd_id
            self.device_list.append(water_device)

    def add_power_socket(self, name, room, ):
        self.logger.info("Create power socket with name {}.".format(name))
        power_socket = PowerSocket(name, room, self.sql_controller, self.logger, self.flag)
        ps_id = self.sql_controller.check_power_socket(name)
        if ps_id is None:
            ps_id = self.sql_controller.insert_into_power_sockets(power_socket)
            if ps_id is not None:
                power_socket.ps_id = ps_id
                self.device_list.append(power_socket)
            else:
                self.logger.warn("Removing {}".format(power_socket.name))
                del power_socket
        else:
            power_socket.ps_id = ps_id
            self.device_list.append(power_socket)

    def add_light_bulb(self, name, _type, brand, room):
        self.logger.info("Create light bulb.")
        light_bulb = LightBulb(name, _type, brand, room, self.sql_controller, self.logger, self.flag)
        lb_id = self.sql_controller.check_light_bulb(name)
        if lb_id is None:
            lb_id = self.sql_controller.insert_into_light_bulbs(light_bulb)
            if lb_id is not None:
                light_bulb.lb_id = lb_id
                self.device_list.append(light_bulb)
            else:
                self.logger.warn("Removing {}".format(light_bulb.name))
                del light_bulb
        else:
            light_bulb.lb_id = lb_id
            level_of_consumption = self.sql_controller.get_bulb_level_of_consumption(lb_id)
            light_bulb.level_of_consumption = level_of_consumption if level_of_consumption is not None else 100
            self.device_list.append(light_bulb)

    def add_sensor(self, sensor_type, room):
        self.logger.info("Create sensor {}.".format(sensor_type))
        if sensor_type == SensorType.temperature_sensor:
            sensor = TemperatureSensor(room, self.sql_controller, self.logger, sensor_type, self.flag)
        elif sensor_type == SensorType.humidity_sensor:
            sensor = HumilitySensor(room, self.sql_controller, self.logger, sensor_type, self.flag)
        elif sensor_type == SensorType.smoke_sensor:
            sensor = SmokeSensor(room, self.sql_controller, self.logger, sensor_type, self.flag)
        else:
            raise ValueError("Wrong sensor type, sensor not created.")
        self.sensor_list.append(sensor)

    def start_devises(self):
        self.logger.warn("Starting all devices.")
        if self.device_list:
            for device in self.device_list:
                t = threading.Thread(target=device.check_status_start)
                self.device_thread_list.append({device.name: t})
                t.start()
                sleep(1)
        else:
            self.logger.warn("No created devices.")

    def stop_devises(self):
        self.logger.warn("Stopping all devices.")
        if self.device_list:
            for device in self.device_list:
                device.flag = False
            for thread in self.device_thread_list:
                thread.values().join()
        else:
            self.logger.warn("No created devices, Nothing to stop.")

    def start_sensors(self):
        self.logger.warn("Starting all sensors.")
        if self.sensor_list:
            for sensor in self.sensor_list:
                t = threading.Thread(target=sensor.start_sensor)
                self.sensor_thread_list.append(t)
                t.start()
                sleep(1)
        else:
            self.logger.warn("No created sensors.")

    def stop_sensors(self):
        self.logger.warn("Stopping all sensors.")
        if self.sensor_list:
            for sensor in self.sensor_list:
                sensor.set_flag(False)
            for thread in self.sensor_thread_list:
                thread.join()

        else:
            self.logger.warn("No created sensors, Nothing to stop.")

    def disconnect_sql(self):
        self.sql_controller.disconnect()

    def stop_day(self):
        self.logger.warn("Stop day.")
        self.day.flag = False
        self.day_thread.join()

    def delete_device_by_name(self, name):
        self.logger.warn("try to delete device: {}".format(name))
        is_removed = False
        for device in self.device_list:
            if device.name == name:
                is_removed = True
                del device
                self.logger.warn("Device: {} removed".format(name))
                break
        if is_removed:
            self.sql_controller.delete_device(name)
        else:
            self.logger.critical("Device with name {} didnt find!".format(name))
