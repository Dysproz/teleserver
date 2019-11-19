import dash_html_components as html
import layouts.style.style as style
from tools.calendar_generation import calendar_config
import dash_core_components as dcc

def change_calendar_content():
    """
    Create layout for calendar

    :return: Layout with 1 second refresh interval
    :rtype: dash.development.base_component.ComponentMeta
    """
    calendarID = calendar_config()
    return html.Div([
        html.Iframe(
                   src='https://calendar.google.com/calendar/embed?src={}&ctz=Europe%2FWarsaw&hl=en_GB'.format(calendarID),
                   width='1000',
                   height='600'
        ),
        html.H4('Event title'),
        dcc.Input(
                 id='event-title',
                 type='text',
                 value='Desk reservation'
        ),
        html.H4('Choose a date of a reservation'),
        dcc.DatePickerRange(
                           id='date-picker-range'
        ),
        html.H4('Starting and ending time of reservation'),
        dcc.RangeSlider(
                       id='time_slider',
                       count=1,
                       min=0,
                       max=23*60+59,
                       step=1,
                       value=[0, 23*60+59]
        ),
        html.Button(
                   id='time-submit-button',
                   n_clicks = 0,
                   children='Add an event'
        )], style={'margin': style.PADDING})
