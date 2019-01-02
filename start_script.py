from time import sleep

from home_controller import HomeController
from simulators.enum import SensorType, Rooms

if __name__ == '__main__':

    home_controller = HomeController()
    sleep(5)
    home_controller.add_sensor(SensorType.temperature_sensor, Rooms.bathroom)
    home_controller.add_sensor(SensorType.humidity_sensor, Rooms.bathroom)
    home_controller.add_sensor(SensorType.smoke_sensor, Rooms.bathroom)
    home_controller.add_light_bulb("Zarowka","LED", "DobraMarka", Rooms.bathroom)
    home_controller.add_power_socket("Gniazdo1", Rooms.bathroom)
    home_controller.add_water_device("Pralka_KEK", "Pralka_KEK", "Samsung", Rooms.bathroom)

    home_controller.start_devises()
    home_controller.start_sensors()

    sleep(14400)

    home_controller.stop_devises()
    home_controller.stop_sensors()
    home_controller.stop_day()
    home_controller.delete_device_by_name("Zarowka")
    home_controller.delete_device_by_name("Pralka_KEK")
    home_controller.disconnect_sql()
