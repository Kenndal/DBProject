def get_light_bulbs_status(sql_controller, room):
    light_bulbs_status = []
    light_bulbs = sql_controller.get_all_bulbs_from_room(room)
    for light_bulb in light_bulbs:
        light_bulb_status = sql_controller.get_light_bulb_status(light_bulb[0])
        if light_bulb_status:
            light_bulbs_status.append({'name': light_bulb[2],
                                       'type': light_bulb[3],
                                       'brand': light_bulb[4],
                                       'level_of_consumption': light_bulb_status[-1][2],
                                       'power_consumption': light_bulb_status[-1][3]})
        else:
            light_bulbs_status.append({'name': light_bulb[2],
                                       'type': light_bulb[3],
                                       'brand': light_bulb[4],
                                       'level_of_consumption': "None",
                                       'power_consumption': "None"})
    return light_bulbs_status



def get_power_socket_status(sql_controller, room):
    power_sockets_status = []
    power_socktes = sql_controller.get_power_sockets_from_room(room)

    for power_socket in power_socktes:
        power_socket_status = sql_controller.get_power_sockets_status(power_socket[0])
        if power_socket_status:
            power_sockets_status.append({'name': power_socket[2],
                                         'power_consumption': power_socket_status[-1][2]})
        else:
            power_sockets_status.append({'name': power_socket[2],
                                         'power_consumption': "None"})

    return power_sockets_status

