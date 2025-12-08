"""
Reminder Module - Manages user reminders and notifications

Features:
- Set reminders for specific times/dates
- List all reminders
- Delete reminders
- Get reminded at scheduled time
"""

import json
import os
from datetime import datetime, timedelta
import pytz

REMINDERS_FILE = "reminders.json"

def load_reminders():
    """Load all reminders from file"""
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_reminders(reminders):
    """Save reminders to file"""
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=2)

def add_reminder(user_id, text, remind_time):
    """
    Add a new reminder for user
    
    Args:
        user_id: Telegram user ID
        text: Reminder text (what to remind about)
        remind_time: datetime object when to remind
    
    Returns:
        reminder_id: Unique ID for the reminder
    """
    reminders = load_reminders()
    user_id_str = str(user_id)
    
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
    """Get all active reminders for a user"""
    reminders = load_reminders()
    user_id_str = str(user_id)
    
    if user_id_str not in reminders:
        return []
    
    # Filter out completed reminders
    return [r for r in reminders[user_id_str] if not r.get("completed", False)]

def delete_reminder(user_id, reminder_id):
    """Delete a reminder by ID"""
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
    """Format reminder for display"""
    try:
        remind_time = datetime.fromisoformat(reminder["time"])
        time_str = remind_time.strftime("%Y-%m-%d %H:%M")
    except:
        time_str = reminder["time"]
    
    return f"🔔 {reminder['id']}. {reminder['text']} - {time_str}"

def get_due_reminders():
    """Get all reminders that are due now (within 1 minute)"""
    reminders = load_reminders()
    due = {}
    now = datetime.now()
    
    for user_id_str, user_reminders in reminders.items():
        for reminder in user_reminders:
            if reminder.get("completed"):
                continue
            
            try:
                remind_time = datetime.fromisoformat(reminder["time"])
                # Check if reminder is due (within 1 minute window)
                if remind_time <= now and (now - remind_time).total_seconds() < 60:
                    if user_id_str not in due:
                        due[user_id_str] = []
                    due[user_id_str].append(reminder)
            except:
                pass
    
    return due

def mark_completed(user_id, reminder_id):
    """Mark a reminder as completed"""
    reminders = load_reminders()
    user_id_str = str(user_id)
    
    if user_id_str in reminders:
        for reminder in reminders[user_id_str]:
            if reminder.get("id") == reminder_id:
                reminder["completed"] = True
                save_reminders(reminders)
                return True
    
    return False

def parse_time_input(time_str):
    """
    Parse user time input in various formats
    
    Formats supported:
    - "14:30" → Today at 14:30
    - "tomorrow 10:00" → Tomorrow at 10:00
    - "in 30 minutes" → 30 minutes from now
    - "2025-12-25 18:00" → Specific date and time
    """
    time_str = time_str.lower().strip()
    now = datetime.now()
    
    # Format: "14:30"
    if ":" in time_str and ":" not in time_str.replace(":", "", 1):
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            result = datetime.combine(now.date(), time_obj)
            # If time is in the past today, assume tomorrow
            if result < now:
                result += timedelta(days=1)
            return result
        except:
            return None
    
    # Format: "tomorrow 10:00"
    if "tomorrow" in time_str:
        time_str = time_str.replace("tomorrow", "").strip()
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            result = datetime.combine(now.date() + timedelta(days=1), time_obj)
            return result
        except:
            return None
    
    # Format: "in 30 minutes"
    if "in" in time_str and "minute" in time_str:
        try:
            minutes = int(time_str.split("in")[1].split("minute")[0].strip())
            return now + timedelta(minutes=minutes)
        except:
            return None
    
    # Format: "2025-12-25 18:00"
    try:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    except:
        return None

# Timezone for display
def get_timezone():
    """Get user's timezone (hardcoded to Finland for now)"""
    return pytz.timezone("Europe/Helsinki")
