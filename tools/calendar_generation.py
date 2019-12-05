from __future__ import print_function
import pickle
import os.path
import yaml
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from os import path

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def initializeCalendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    :return: connection to a Google Calendar
    :rtype: googleapiclient.discovery.Resource
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
    print(type(CAL))
    return CAL


def sendToGoogleCalendar(start_date, end_date, hours, minutes, event_title):
    """
    Send an event to Google Calendar using Calendar API.
    :param start_date: Start date of an event
    :param end_date: End date of an event
    :param hours: List with start and end hour of an event
    :param minutes: List with start and end minute of an event
    :param event_title: Title of added event
    :return: Boolean value - success or failure of adding event
    :rtype: Boolean
    """
    try:
        CAL = initializeCalendar()
        # Call the Calendar API
        GMT_OFF = '+01:00'
        EVENT = {
            'summary': '{}'.format(event_title),
            'start':  {'dateTime': '{}T{}:{}:00%s'.format(start_date, hours[0], minutes[0]) % GMT_OFF},
            'end':    {'dateTime': '{}T{}:{}:00%s'.format(end_date, hours[1], minutes[1]) % GMT_OFF},
        }
        result = calendar_config()
        CAL.events().insert(calendarId=result[2], sendNotifications=False, body=EVENT).execute()
        return True
    except Exception:
        return False


def calendar_config():
    '''
    Open a configuration file and read iframe,
    file with credentials for Calendar API and
    calendarID
    :return: List with iframe, api_credentials, calendarID strings
    :rtype: List
    '''
    if(path.exists("config.yml")):
        with open('config.yml', 'r') as file_config:
            content = yaml.load(file_config)
        if 'calendar' in content:
            iframe = content['calendar'].get('iframe', None)
            api_credentials = content['calendar'].get('api_credentials', None)
            calendarID = content['calendar'].get('calendarID', None)
            return iframe, api_credentials, calendarID
        else:
            return 3*[None]
    else:
        return 3*[None]
