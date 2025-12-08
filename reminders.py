import json
import os
from datetime import datetime, timedelta
import pytz

REMINDERS_FILE = "reminders.json"


def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)


def add_reminder(user_id, text, remind_time):
    reminders = load_reminders()
    uid = str(user_id)

    if uid not in reminders:
        reminders[uid] = []

    reminder_id = len(reminders[uid]) + 1

    reminder = {
        "id": reminder_id,
        "text": text,
        "time": remind_time.isoformat(),
        "created_at": datetime.now().isoformat(),
        "completed": False
    }

    reminders[uid].append(reminder)
    save_reminders(reminders)

    return reminder_id


def get_user_reminders(user_id):
    reminders = load_reminders()
    uid = str(user_id)

    if uid not in reminders:
        return []

    return [r for r in reminders[uid] if not r.get("completed", False)]


def delete_reminder(user_id, reminder_id):
    reminders = load_reminders()
    uid = str(user_id)

    if uid in reminders:
        reminders[uid] = [r for r in reminders[uid] if r.get("id") != reminder_id]
        save_reminders(reminders)
        return True

    return False


def mark_completed(user_id, reminder_id):
    reminders = load_reminders()
    uid = str(user_id)

    if uid in reminders:
        for r in reminders[uid]:
            if r.get("id") == reminder_id:
                r["completed"] = True
                save_reminders(reminders)
                return True

    return False


def get_due_reminders():
    reminders = load_reminders()
    now = datetime.now()
    due = {}

    for uid, user_reminders in reminders.items():
        for r in user_reminders:
            if r.get("completed"):
                continue

            try:
                t = datetime.fromisoformat(r["time"])
                diff = (now - t).total_seconds()

                if 0 <= diff < 60:
                    if uid not in due:
                        due[uid] = []
                    due[uid].append(r)

            except:
                pass

    return due


def parse_time_input(time_str):
    time_str = time_str.lower().strip()
    now = datetime.now()

    if "second" in time_str:
        try:
            sec = int(time_str.split()[0])
            return now + timedelta(seconds=sec)
        except:
            return None

    if ":" in time_str and time_str.count(":") == 1:
        try:
            t = datetime.strptime(time_str, "%H:%M").time()
            dt = datetime.combine(now.date(), t)
            if dt < now:
                dt += timedelta(days=1)
            return dt
        except:
            return None

    if "tomorrow" in time_str:
        try:
            t = time_str.replace("tomorrow", "").strip()
            t = datetime.strptime(t, "%H:%M").time()
            return datetime.combine(now.date() + timedelta(days=1), t)
        except:
            return None

    if "in" in time_str and "minute" in time_str:
        try:
            minutes = int(time_str.split("minute")[0].split("in")[1].strip())
            return now + timedelta(minutes=minutes)
        except:
            return None

    try:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    except:
        return None


def format_reminder(r):
    try:
        t = datetime.fromisoformat(r["time"])
        ts = t.strftime("%Y-%m-%d %H:%M")
    except:
        ts = r["time"]

    return f"{r['id']}. {r['text']} - {ts}"


def get_timezone():
    return pytz.timezone("Europe/Helsinki")
