import json
import os

DB_USERS = "users.json"

def load_users():

    try:
        with open(DB_USERS, "r") as f:
            return json.load(f)
    except(json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    with open(DB_USERS, "w") as f:
        json.dump(users, f, indent=2)


def add_user(user_id, userName=None):
    users = load_users()
    users[str(user_id)] = {
        "username": userName,
        "location": {
            "latitude": "",
            "longitude": ""
        }
    }
    save_users(users)

def save_user_location(user_id, lat, long):
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {"username": None, "location": {}}

    users[str(user_id)]["location"] = {
        "latitude": lat,
        "longitude": long
    }

    save_users(users)


def get_user_location(user_id):
    users = load_users()
    return users[str(user_id)]["location"]

