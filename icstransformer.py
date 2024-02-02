#!/bin/env python3
import jicson
import json 
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





def main():
    allevents = readCalendar()
    print("Habe so viele Termine gefunden: " + str(len(allevents)))

    today = datetime.now()
    events = filterByDate(allevents, today.year, today.month, today.day)
    printEvents(events)


if __name__ == "__main__":
    main()
