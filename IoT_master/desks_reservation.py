import datetime

from tools.desks_reservation_func import initializeCalendar, calendar_config
from tmp_tab import desk_reservations

if __name__ == '__main__':
    CAL = initializeCalendar()
    page_token = None
    result = calendar_config()
    time_min = datetime.datetime.now() - datetime.timedelta(days=5)
    time_min = time_min.strftime('%Y-%m-%dT%H:%M:%S+01:00')
    while True:
        events = CAL.events().list(calendarId=result[2], pageToken=page_token, timeMin=time_min).execute()
        for event in events['items']:
            title = str(event['summary']).split()
            event_id = str(event['id'])
            # Desk number taken from event title
            table_index = int(title[1])-1
            start_time = str(event['start']['dateTime']).split('+')
            end_time = str(event['end']['dateTime']).split('+')
            # Start time and date of an event
            start_time = datetime.datetime.strptime(start_time[0], '%Y-%m-%dT%H:%M:%S')
            # End time and date of an event
            end_time = datetime.datetime.strptime(end_time[0], '%Y-%m-%dT%H:%M:%S')
            # Start time and date of now - 10 minutes - time given for reservation
            now = datetime.datetime.now()
            now_10 = now - datetime.timedelta(minutes=10)
            if(now_10 >= start_time and now <= end_time and desk_reservations[table_index] == 0):
                # Checks if desk is reserved
                # Delete an event if it is reserved but no one is sitting at the desk
                CAL.events().delete(calendarId=result[2], eventId=event_id).execute()
        page_token = events.get('nextPageToken')
        if not page_token:
            break
