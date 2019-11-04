import dash_core_components as dcc
import dash_html_components as html
import layouts.style.style as style
import calendar
from tools.calendar_generation import generate_month
from tools.calendar_generation import print_title

CAL_BUT = [
        [
           'Previous'
	],
        [
           'Next'
        ]
]

def change_calendar_content():
   """
   Create layout for calendar
   
   :return: Layout with 1 second refresh interval
   :rtype: dash.development.base_component.ComponentMeta
   """
   return html.Div([
        html.Div(id='live-calendar'),
        html.Div(id='calendar-output'),
        dcc.Interval(
            id='calendar-interval-component', interval=1000, n_intervals=0)
        ], style={'margin': style.PADDING})

def create_all_calendar():
   """
   Create all content for a calendar (one month)
   
   :return: Output from create_calendar_content function and title of a calendar
   :rtype: dash.development.base_component.ComponentMeta
   """
   return html.Div(
      [
         html.H1('Desk reservations'),
         html.H2(print_title()),
         create_calendar_content()
      ])

def create_calendar_content():
    """
    Create buttons for a calendar - with days and switching months
    
    :return: Buttons with days of the month and switching months buttons
    :rtype: dash.development.base_component.ComponentMeta
    """
    calendar_buttons = []
    new_calendar = generate_month()
    change_month_layout = []
    for calbuttons in CAL_BUT:
         for key in calbuttons:
            change_month_layout.append(
            html.Button(
            id='{}-change_mth'.format(key),
            n_clicks=0,
            children=calbuttons,
            style={
                   'margin': style.PADDING,
                   'backgroundColor': style.BUTTON_COLOR
                }))
    calendar_buttons.append(html.Div(change_month_layout))

    for line in new_calendar:
         line_layout = []
         for key in line:
            line_layout.append(
                html.Button(
                id='{}-cal_button'.format(key),
                children=key,
                style={
                   'margin': style.PADDING,
                   'backgroundColor': style.BUTTON_COLOR
		}))
         calendar_buttons.append(html.Div(line_layout))
    return html.Div(calendar_buttons)

