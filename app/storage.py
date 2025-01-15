import json

# ХД юзеров
users = {}

def save_data():
    with open("users_data.json", "w") as file:
        json.dump(users, file)

def load_data():
    global users
    try:
        with open("users_data.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}
        save_data()