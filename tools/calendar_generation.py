from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import calendar
from os import path

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def initializeCalendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
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
            result = calendar_config()
            flow = InstalledAppFlow.from_client_secrets_file(
                result[1], SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    CAL = build('calendar', 'v3', credentials=creds)
    return CAL


def sendToGoogleCalendar(start_date, end_date, hours, minutes, event_title):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    try:
        CAL = initializeCalendar()
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        GMT_OFF = '+01:00'
        EVENT = {
            'summary': '{}'.format(event_title),
            'start':  {'dateTime': '{}T{}:{}:00%s'.format(start_date, hours[0], minutes[0]) %GMT_OFF},
            'end':    {'dateTime': '{}T{}:{}:00%s'.format(end_date, hours[1], minutes[1]) %GMT_OFF},
        }
        result = calendar_config()
        e = CAL.events().insert(calendarId=result[2], sendNotifications=False, body=EVENT).execute()
        return True
    except:
        return False


def calendar_config():
    if(path.exists("config.yml")):
        file_config = open("config.yml","r")
        result = []
        for content in file_config:
            content = content.split()
            if content is not None:
                if(content[0]=="iframe:"):
                    result.append(content[1])
                if(content[0]=="api_credentials:"):
                    result.append(content[1])
                if(content[0]=="calendarID:"):
                    result.append(content[1])
        file_config.close()
        return result
    else:
        print("The configuration file calendar.conf does not exist")

