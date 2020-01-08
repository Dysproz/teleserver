from __future__ import print_function
import pickle
import yaml
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from os import path

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def initializeCalendar():
    """Initialize a Google Calendar API
    :return: Connection to Calendar
    :rtype: googleapiclient.discovery.Resource
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if path.exists('token.pickle'):
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


def sendToGoogleCalendar(start_date, end_date, hours, minutes, event_title, CAL):
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
            desks = content['calendar'].get('desks', None)
            return iframe, api_credentials, calendarID, desks
        else:
            return 4*[None]
    else:
        return 4*[None]


def desk_combobox():
    '''
    Add labels to combobox dynamically due to number of desks
    in config.yml file
    :return: List with labels
    :rtype: List
    '''
    result_config = calendar_config()
    options = []
    for x in range(int(result_config[3])):
        options.append({'label': 'Desk {}'.format(x+1), 'value': 'Desk {}'.format(x+1)})
    return options


def desk_available(CAL, desk_number, desk_reservations):
    '''
    Check if chosen desk is available due to list with reserved desks
    and calendar
    :return: Boolean with information of desk availability
    :rtype: Boolean
    '''
    page_token = None
    result = calendar_config()
    time_min = datetime.datetime.now() - datetime.timedelta(days=5)
    time_min = time_min.strftime('%Y-%m-%dT%H:%M:%S+01:00')
    while True:
        events = CAL.events().list(calendarId=result[2], pageToken=page_token, timeMin=time_min).execute()
        for event in events['items']:
            title = str(event['summary']).split()
            # Desk number taken from event title
            table_index = int(title[1])-1
            start_time = str(event['start']['dateTime']).split('+')
            end_time = str(event['end']['dateTime']).split('+')
            # Start time and date of an event
            start_time = datetime.datetime.strptime(start_time[0], '%Y-%m-%dT%H:%M:%S')
            # End time and date of an event
            end_time = datetime.datetime.strptime(end_time[0], '%Y-%m-%dT%H:%M:%S')
            now = datetime.datetime.now()
            if now >= start_time and now <= end_time \
               and desk_reservations[table_index] == 1 and title[1] == desk_number:
                return False
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    return True
