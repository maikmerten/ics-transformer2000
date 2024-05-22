#!/bin/env python3
import jicson
import json 
import requests
from datetime import datetime

def readCalendar():
    allevents = []
    result = jicson.fromFile('./input.ics')
    calendar = result["VCALENDAR"]

    for i in range(0, len(calendar)):
        events = calendar[i]["VEVENT"]

        for event in events:
            keys = event.keys()
            description = ""
            start = ""
            end = ""

            for key in keys:
                if key.startswith("DTSTART"):
                    start = event[key]
                elif key.startswith("DTEND"):
                    end = event[key]
                elif key.startswith("DESCRIPTION"):
                    description = event[key]

            start = datetime.strptime(start, "%Y%m%dT%H%M%S")
            end = datetime.strptime(end, "%Y%m%dT%H%M%S")
            myEvent = {
                "start": start,
                "end": end,
                "description": description
            }
            allevents.append(myEvent)
    
    return allevents

def filterByDate(events, year, month, day):
    filterEvents = []
    for event in events:
        start = event["start"]
        if start.year == year and start.month == month and start.day == day:
            filterEvents.append(event)
    
    return filterEvents

def printEvents(events):
    for event in events:
        print(event["description"] + "  " + str(event["start"]) + " -> " + str(event["end"]))

def makeScheduleObj(room, date, events, mac):

    entries = []
    for event in events:
        entry = []
        entry.append(str(event["start"]) + "-" + str(event["end"]))
        entry.append(event["description"])
        entries.append(entry)

    schedule = {
        "room": room,
        "date": date,
        "entries": entries
    }

    envelope = {
        "mac": mac,
        "schedule": schedule
    }

    return envelope 

def uploadJson(obj):
    session = requests.Session()

    credentials = { # test credentials for public consumption (in secure sandbox)
        "user": "test",
        "password": "sesame"
    }
    x = session.post("http://localhost:8000/api/login", json=credentials)
    print(x.text)

    url = "http://localhost:8000/api/upload-schedule"
    x = session.post(url=url, json=obj)
    print(x.text)

def main():
    allevents = readCalendar()
    print("Habe so viele Termine gefunden: " + str(len(allevents)))

    today = datetime.now()
    events = filterByDate(allevents, today.year, today.month, today.day)
    printEvents(events)

    events = filterByDate(allevents, 2024, 3, 11)
    printEvents(events)

    room = "Raum 237"
    mac = "0000021E733A7430"
    date = "23.07.1980"

    schedul_obj = makeScheduleObj(room, date, events, mac)
    #json_string = json.dumps(schedul_obj)
    #print(json_string)
    uploadJson(schedul_obj)


if __name__ == "__main__":
    main()
