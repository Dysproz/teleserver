import dash_core_components as dcc
import dash_html_components as html
import layouts.style.style as style
from tools.calendar_generation import generate_month
from tools.calendar_generation import print_title

CAL_BUT = ['Previous', 'Next']


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


def create_all_calendar(CalTimeObject):
    """
    Create all content for a calendar (one month)

    :param CalTimeObject: Object with month, year, name of the month
    :return: Output from create_calendar_content function and title of a calendar
    :rtype: dash.development.base_component.ComponentMeta
    """
    return html.Div(
        [
            html.H1('Desk reservations'),
            html.H2(print_title(CalTimeObject)),
            create_calendar_content(CalTimeObject)
        ])


def create_calendar_content(CalTimeObject):
    """
    Create buttons for a calendar - with days and switching months

    :param CalTimeObject: Object with month, year, name of the month
    :return: Buttons with days of the month and switching months buttons
    :rtype: dash.development.base_component.ComponentMeta
    """
    calendar_buttons = []
    new_calendar = generate_month(CalTimeObject)
    change_month_layout = []
    for key in CAL_BUT:
        change_month_layout.append(
                                  html.Button(
                                             id='{}-change_mth'.format(key),
                                             n_clicks=0,
                                             children=key,
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
