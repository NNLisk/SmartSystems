import requests
from icalendar import Calendar
from datetime import datetime, date
import zoneinfo
import userbase

def getCalendar(inputurl):
    url = inputurl
    response = requests.get(url)
    ics = response.text
    print("calendar got")
    cal = parse_calendar(ics)
    print(cal)
    return cal

def parse_calendar(calendar):
    print("parsing calendar")
    cal = Calendar.from_ical(calendar)
    events = []

    for component in cal.walk():
        if component.name == "VEVENT":
            summary = component.get("SUMMARY")
            start = component.decoded("DTSTART")
            location = component.get("LOCATION")
            # print(summary)
            
            events.append({
                "summary": summary,
                "start": start,
                "location": location
            })
            # print("appended")
    
    # print(events)
    return events

def get_todays_events(user_id):
    usersurl = userbase.get_calendar_url(user_id)

    if usersurl is None or usersurl == "":
        print("nourl")
        return []

    events = getCalendar(usersurl)
    # today = datetime.now(zoneinfo.ZoneInfo("Europe/Helsinki")).date()
    today = date(2025, 12, 4)
    todays_events = []

    for e in events:
        start_utc = e["start"]
        start_local = start_utc.astimezone(zoneinfo.ZoneInfo("Europe/Helsinki"))
        if start_local.date() == today:
            print("found on date")
            todays_events.append(e)

    message = format_message(todays_events)
    return message


def format_message(events):
    if not events:
        return "no lectures today"

    msg = ""

    for e in events:
        start = e["start"]
        summary = str(e.get("summary", "no title"))
        location = str(e.get("location", "no location given"))

        msg += f"{summary}\n{start}\n{location}\n\n"

    return msg



if __name__ == "__main__":
    getCalendar("https://sisu.lut.fi:443/ilmo/api/calendar-share/846986e1-14c1-405c-885e-87f68b1c9ab1")
