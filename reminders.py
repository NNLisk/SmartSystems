import json
import os
from datetime import datetime, timedelta
import pytz

REMINDERS_FILE = "reminders.json"

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_reminders(reminders):
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=2)

def add_reminder(user_id, text, remind_time):
def add_reminder(user_id, text, remind_time):
    reminders = load_reminders()
    
    if user_id_str not in reminders:
        reminders[user_id_str] = []
    
    reminder_id = len(reminders[user_id_str]) + 1
    
    reminder = {
        "id": reminder_id,
        "text": text,
        "time": remind_time.isoformat(),
        "created_at": datetime.now().isoformat(),
        "completed": False
    }
    
    reminders[user_id_str].append(reminder)
    save_reminders(reminders)
    
    return reminder_id

def get_user_reminders(user_id):
    reminders = load_reminders()
    user_id_str = str(user_id)
    
    if user_id_str not in reminders:
        return []
    
    return [r for r in reminders[user_id_str] if not r.get("completed", False)]

def delete_reminder(user_id, reminder_id):
    reminders = load_reminders()
    user_id_str = str(user_id)
    
    if user_id_str in reminders:
        reminders[user_id_str] = [
            r for r in reminders[user_id_str] 
            if r.get("id") != reminder_id
        ]
        save_reminders(reminders)
        return True
    
    return False

def format_reminder(reminder):
def format_reminder(reminder):
    try:remind_time = datetime.fromisoformat(reminder["time"])
        time_str = remind_time.strftime("%Y-%m-%d %H:%M")
    except:
        time_str = reminder["time"]
    
    return f"🔔 {reminder['id']}. {reminder['text']} - {time_str}"

def get_due_reminders():
def get_due_reminders():
    reminders = load_reminders()
    now = datetime.now()
    
    for user_id_str, user_reminders in reminders.items():
        for reminder in user_reminders:
            if reminder.get("completed"):
                continue
            
            try:
                remind_time = datetime.fromisoformat(reminder["time"])
                if remind_time <= now and (now - remind_time).total_seconds() < 60:
                    if user_id_str not in due:
                        due[user_id_str] = []
                    due[user_id_str].append(reminder)
            except:
                pass
    
    return due

def mark_completed(user_id, reminder_id):
def mark_completed(user_id, reminder_id):
    reminders = load_reminders()
    
    if user_id_str in reminders:
        for reminder in reminders[user_id_str]:
            if reminder.get("id") == reminder_id:
                reminder["completed"] = True
                save_reminders(reminders)
                return True
    
    return False

def parse_time_input(time_str):
    """
def parse_time_input(time_str):
    time_str = time_str.lower().strip()
    if ":" in time_str and ":" not in time_str.replace(":", "", 1):
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            result = datetime.combine(now.date(), time_obj)
            # If time is in the past today, assume tomorrow
            if result < now:medelta(days=1)
            return result
        except:
            return None
    
    # Format: "tomorrow 10:00"
    if "tomorrow" in time_str:place("tomorrow", "").strip()
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            result = datetime.combine(now.date() + timedelta(days=1), time_obj)
            return result
        except:
            return None
    
    # Format: "in 30 minutes"
    if "in" in time_str and "minute" in time_str:
    if "in" in time_str and "minute" in time_str:.split("minute")[0].strip())
            return now + timedelta(minutes=minutes)
        except:
            return None
    
    # Format: "2025-12-25 18:00"
    try:
    try:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M")

# Timezone for display
def get_timezone():
    """Get user's timezone (hardcoded to Finland for now)"""
    return pytz.timezone("Europe/Helsinki")
def get_timezone():
    return pytz.timezone("Europe/Helsinki")