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
    #calendarID = calendar_config()
    result = calendar_config()
    return html.Div([
        dcc.ConfirmDialog(
                         id='confirm-good',
                         message='Event added',
        ),
        dcc.ConfirmDialog(
                         id='confirm-bad',
                         message='There was an error during adding an event. Please check server logs for an error.',
        ),

        html.Iframe(
                   src=result[0],
                   #src='https://calendar.google.com/calendar/embed?src={}%40group.calendar.google.com&ctz=Europe%2FWarsaw&hl=en_GB'.format(calendarID),
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
        html.Div([
                dcc.DatePickerRange(
                                   id='date-picker-range'
        )], style={'margin': '10px 5px 10px 5px'}),
        html.H4('Hour (start and end)  of reservation:',
               style={'margin': '20px 5px 20px 5px'}),
        dcc.RangeSlider(
                       id='hour-slider',
                       count=1,
                       min=0,
                       max=23,
                       step=1,
                       marks={
                             0: '0',
                             6: '6',
                             12: '12',
                             18: '18',
                             23: '23'
                       },
                       value=[0, 23]
                       ),
        html.Div(id='divider',
                 style={
                        'margin': '20px 5px 20px 5px'
                }),
        html.H4('Minutes (start and end) of reservation',
               style={'margin': '20px 5px 20px 5px'}),
        dcc.RangeSlider(
                       id='minute-slider',
                       count=1,
                       min=0,
                       max=59,
                       step=1,
                       marks={
                             0: '0',
                             15: '15',
                             30: '30',
                             45: '45',
                             59: '59'
                       },
                       value=[0, 59]
        ),
        html.Div(id='divider',
                 style={
                        'margin': '40px 5px 40px 5px'
                }),
        html.Button(
                   id='time-submit-button',
                   n_clicks = 0,
                   children='Add an event'
        )], style={'margin': style.PADDING})
