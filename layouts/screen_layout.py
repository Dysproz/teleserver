import dash_core_components as dcc
import dash_html_components as html

import layouts.style.style as style


def create_screen_content():
    return html.Div([
        html.Div(id='live-screen'),
        dcc.Interval(
            id='screen-interval-component', interval=1000, n_intervals=0)
    ], style={'margin': style.PADDING})
