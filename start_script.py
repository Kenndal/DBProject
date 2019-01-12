from time import sleep

import init_devices
from home_controller import HomeController
from simulators.enum import SensorType, Rooms

if __name__ == '__main__':

    home_controller = HomeController()
    sleep(5)
    init_devices.init(home_controller)

    home_controller.start_devises()
    home_controller.start_sensors()

    sleep(86400*4)

    home_controller.stop_devises()
    home_controller.stop_sensors()
    home_controller.stop_day()
    home_controller.disconnect_sql()
