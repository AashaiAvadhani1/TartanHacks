from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
import calendarExport as cal
import copy
creds = None
SCOPES = ['https://www.googleapis.com/auth.calendar']
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_557209563886-cbb1b5mh49vl17uk1jnecb491io8dmi0.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_local_server()
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)




def writeToFile(names, dates, beginTimes, endTimes, locations, keywords):
    with open("event.csv", mode="w") as employFile:
        writeObject = csv.writer(employFile,delimiter=',')
        writeObject.writerow(["Name", "Date", "Start Time", "End Time", "Location", "Keywords"])
        for i in range(len(names)):
            writeObject.writerow([names[i],dates[i],beginTimes[i],endTimes[i],locations[i], keywords[i]])

# writeToFile(["joe1"],["joe2"],["joe3"],["joe4,"],["j,oe5"],["joe6"])

def readFromFile(filename):
    with open(filename, mode = "r") as eventFile:
        readObj = csv.reader(eventFile, delimiter = ",")
        it = 0
        data = []
        lineLen = 0
        for row in readObj:
            if it == 0:
                lineLen = len(row)
                for i in range(len(row)):
                    data.append([row[i]])
            else:
                for i in range(lineLen):
                    data[i].append(row[i])
            it+=1

        return data

#print(readFromFile("event.csv"))

event = {
  'summary': '',
  'location': 'Somewhere',
  'organizer': {
    'email': '',
    'displayName': ''
  },
  'start': {
    'dateTime': ''
  },
  'end': {
    'dateTime': ''
  },
  'attendees': [
    {
      'email': '',
      'displayName': '',
    },
    # ...
  ],
  'iCalUID': 'originalUID'
}
def findSpecificInstance(phrase, keywords, event, csv=readFromFile('event.csv')):
    finalEvent = []
    for i in range(len(csv[1])):
        a = copy.deepcopy(event)
        if phrase in csv[0][i]:
            x = csv[1][i]
            y = csv[2][i]
            a['location'] = csv[3][i]
            a['start']['dateTime'] = convertDate(csv[0][i])+cal.convertGoogleTime(x)
            a['end']['dateTime'] = convertDate(csv[0][i])+cal.convertGoogleTime(y)
            finalEvent.append(a)
        elif phrase in csv[1][i]:
            x = csv[1][i]
            y = csv[2][i]
            a['location'] = csv[3][i]
            a['start']['dateTime'] = convertDate(csv[0][i])+cal.convertGoogleTime(x)
            a['end']['dateTime'] = convertDate(csv[0][i])+cal.convertGoogleTime(y)
            finalEvent.append(a)

        elif phrase in csv[2][i]:
            x = csv[1][i]
            y = csv[2][i]
            a['location'] = csv[3][i]
            a['start']['dateTime'] = convertDate(csv[0][i])+cal.convertGoogleTime(x)
            a['end']['dateTime'] = convertDate(csv[0][i])+cal.convertGoogleTime(y)
            finalEvent.append(a)

        elif phrase in csv[3][i] or keywords in csv[3][i]:
            x = csv[1][i]
            y = csv[2][i]
            a['location'] = csv[3][i]
            a['start']['dateTime'] = convertDate(csv[0][i])+cal.convertGoogleTime(x)
            a['end']['dateTime'] = convertDate(csv[0][i])+cal.convertGoogleTime(y)
            finalEvent.append(a)

        elif phrase in csv[4][i] or keywords in csv[4][i]:
            x = csv[1][i]
            y = csv[2][i]
            a['location'] = csv[3][i]
            a['start']['dateTime'] = convertDate(csv[0][i])+cal.convertGoogleTime(x)
            a['end']['dateTime'] = convertDate(csv[0][i])+cal.convertGoogleTime(y)
            finalEvent.append(a)
    return finalEvent

def convertToEvent(event,csv=readFromFile("event.csv")):
    finalEvent = []

    for i in range(1,len(csv[1])):
        a = copy.deepcopy(event)
        if csv[0][i] == '' or csv[1][i] == "" or csv[2][i] == "":
            continue
        x = csv[1][i]
        y = csv[2][i]
        a['location'] = csv[3][i]
        a['start']['dateTime'] = convertDate(csv[0][i])+cal.convertGoogleTime(x)
        a['end']['dateTime'] = convertDate(csv[0][i])+cal.convertGoogleTime(y)
        finalEvent.append(a)
    return finalEvent

def convertDate(date):
    finalDate=date[:4]+'-'+date[4:6]+'-'+date[6:]
    return finalDate

def uploadToCalendar(eventLst):
    for i in range(len(eventLst)):
        imported_event = service.events().import_(calendarId='kqm4plrqthth07eodoqef97t00@group.calendar.google.com', body=eventLst[i]).execute()
    return True

#print imported_event['id']

#uploadToCalendar(convertToEvent(event, csv=readFromFile("event2.csv")))
