

def add_user(sql_controller, name, password):
    sql_controller.create_user(name, password)


def delete_user(sql_controller, name):
    sql_controller.delete_user(name)


def get_users(sql_controller):
    users_data = []
    users = sql_controller.get_users()

    for user in users:
        users_data.append({"name": user[0],
                           'is_admin': True if user[2] == 1 else False})

    return users_data


def get_user(sql_controller, name):
    users = get_users(sql_controller)

    for user in users:
        if name == user['name'].replace(" ", ""):
            return user


def login_user(sql_controller, name, password):
    users = sql_controller.get_users()

    for user in users:
        if name == user[0].replace(" ", "") and password == user[1].replace(" ", ""):
            return True

    return False


def change_password(sql_controller, name, new_password):
    sql_controller.change_password(name, new_password)


def change_name(sql_controller, old_name, new_name):
    sql_controller.change_user_name(old_name, new_name)
