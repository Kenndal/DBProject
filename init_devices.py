
from simulators.enum import SensorType, Rooms


def init(home_controller):

    # Temperature sensors
    home_controller.add_sensor(SensorType.temperature_sensor, Rooms.bathroom)
    home_controller.add_sensor(SensorType.temperature_sensor, Rooms.kitchen)
    home_controller.add_sensor(SensorType.temperature_sensor, Rooms.bedroom)
    home_controller.add_sensor(SensorType.temperature_sensor, Rooms.living_room)
    home_controller.add_sensor(SensorType.temperature_sensor, Rooms.corridor)

    # humidity sensors
    home_controller.add_sensor(SensorType.humidity_sensor, Rooms.bathroom)
    home_controller.add_sensor(SensorType.humidity_sensor, Rooms.kitchen)
    home_controller.add_sensor(SensorType.humidity_sensor, Rooms.bedroom)
    home_controller.add_sensor(SensorType.humidity_sensor, Rooms.living_room)
    home_controller.add_sensor(SensorType.humidity_sensor, Rooms.corridor)

    # smoke sensors
    home_controller.add_sensor(SensorType.smoke_sensor, Rooms.bathroom)
    home_controller.add_sensor(SensorType.smoke_sensor, Rooms.kitchen)
    home_controller.add_sensor(SensorType.smoke_sensor, Rooms.bedroom)
    home_controller.add_sensor(SensorType.smoke_sensor, Rooms.living_room)
    home_controller.add_sensor(SensorType.smoke_sensor, Rooms.corridor)

    # light bulbs
    home_controller.add_light_bulb("Zarowka_lazienka","LED", "DobraMarka", Rooms.bathroom)
    home_controller.add_light_bulb("Zarowka_lazienka_2", "LED", "DobraMarka", Rooms.bathroom)

    home_controller.add_light_bulb("Zarowka_kuchnia", "LED", "DobraMarka", Rooms.kitchen)
    home_controller.add_light_bulb("Zarowka_kuchnia_2", "LED", "DobraMarka", Rooms.kitchen)

    home_controller.add_light_bulb("Zarowka_salon", "LED", "DobraMarka", Rooms.living_room)
    home_controller.add_light_bulb("Zarowka_salon_2", "LED", "DobraMarka", Rooms.living_room)

    home_controller.add_light_bulb("Zarowka_sypialnia", "LED", "DobraMarka", Rooms.bedroom)

    home_controller.add_light_bulb("Zarowka_korytarz", "LED", "DobraMarka", Rooms.corridor)

    # power sockets
    home_controller.add_power_socket("Gniazdo_lazienka", Rooms.bathroom)
    home_controller.add_power_socket("Gniazdo_lazienka_2", Rooms.bathroom)

    home_controller.add_power_socket("Gniazdo_kuchnia", Rooms.kitchen)
    home_controller.add_power_socket("Gniazdo_salon", Rooms.living_room)
    home_controller.add_power_socket("Gniazdo_sypialnia", Rooms.bedroom)
    home_controller.add_power_socket("Gniazdo_korytarz", Rooms.corridor)

    # water devices
    home_controller.add_water_device("Pralka_KEK", "Pralka_KEK", "Samsung", Rooms.bathroom)
    home_controller.add_water_device("Zmywarka", "Zymywarka", "Samsung", Rooms.bathroom)

    # home_controller.save_devices()
    # home_controller.save_sensors()
