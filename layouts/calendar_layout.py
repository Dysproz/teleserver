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
   return html.Div([
        html.Div(id='live-calendar'),
        dcc.Interval(
            id='calendar-interval-componenent', interval=1000, n_intervals=0)
        ])


def create_all_calendar():
   output = html.Div(
      [
         html.H1('Desk reservations'),
         html.H2(print_title()),
         create_calendar_content()
      ])
   return output

def create_calendar_content():
    calendar_buttons = []
    new_calendar = generate_month()
    change_month_layout = []
    for calbuttons in CAL_BUT:
         change_month_layout.append(
            html.Button(
            id='{}-change_mth'.format(calbuttons),
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
         #output = html.Div(
           # [
            #   html.H1(print_title()),
            #   calendar_buttons
            #])
    return html.Div(calendar_buttons)
                 #[
                 #html.H1('Desk reservations'),
                 #html.Table(myCal.formatmonth(2019, 10))
                 #],
                 #style={
            #'margin': style.PADDING,
            #'font-family': 'helvetica',
            #'color': ' #525252',
			#'font-size': '20',
            #'text-align': 'center',
            #'vertical-align': 'text-top',
            #'max-width': '50%',
            #'display': 'inline-block'
        #          })