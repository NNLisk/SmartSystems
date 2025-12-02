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
        "username": userName
    }
    save_users(users)


