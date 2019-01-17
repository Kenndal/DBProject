from time import sleep
from interface.tools import user_management
import init_devices
from home_controller import HomeController

if __name__ == '__main__':

    home_controller = HomeController()
    sleep(5)

    user_management.add_user(home_controller.sql_controller, "kek", "kek")

    init_devices.init(home_controller)

    home_controller.start_devises()
    home_controller.start_sensors()

    sleep(14400)

    home_controller.stop_devises()
    home_controller.stop_sensors()
    home_controller.stop_day()
    home_controller.disconnect_sql()
