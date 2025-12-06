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
        },
        "news-counts": {

        },
        "calendar-url": ""
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

def add_news_count(user_id, category):
    users = load_users()
    count = user.setdefault("news-counts", {})

    counts[category] = counts.get(category, 0) + 1

    save_users(users)

def get_preferred_categories(user_id):
    users = load_users()
    user = users.get(str(user_id), {})
    items = user.get("news-counts", {})
    sorted_items = sorted(items.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    categories = [item[0] for item in sorted_items]
    return categories[:3]

def update_calendar_url(user_id, url):
    users = load_users()
    users[str(user_id)]["calendar-url"] = url
    save_users(users)

def get_calendar_url(user_id):
    users = load_users()
    return users[str(user_id)]["calendar-url"]
