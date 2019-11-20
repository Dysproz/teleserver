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

def sendToGoogleCalendar(start_date, end_date, start_time, end_time, event_title):
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    CAL = build('calendar', 'v3', credentials=creds)
    start_date_h = start_date / 3600
    start_date_m = (start_date - start_date_h) / 60
    end_date_h = end_date / 3600
    end_date_m = (end_date - end_date_h) / 60
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    GMT_OFF = '+01:00'
    EVENT = {
        'summary': '{}'.format(event_title),
        'start':  {'dateTime': '{}T{}:{}:00%s'.format(start_date, start_date_h, start_date_m) %GMT_OFF},
        'end':    {'dateTime': '{}T{}:{}:00%s'.format(end_date, end_date_h, end_date_m) %GMT_OFF},
    }
    calendarID = calendar_config()
    e = CAL.events().insert(calendarId='{}@group.calendar.google.com'.format(calendarID), sendNotifications=False, body=EVENT).execute()
	
def calendar_config():
    if(path.exists("calendar.conf")):
        file_config = open("calendar.conf","r")
        content = file_config.readline()
        content = content.split()
        if(content[0]=="calendarID"):
            return content[2]
    else:
        print("ERROR: The configuration file calendar.conf does not exist")
