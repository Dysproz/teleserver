import dash_core_components as dcc
import dash_html_components as html

import layouts.style.style as style


def create_screen_content():
    """Create screen snapshot layout

    :return: Screen snapshot layout as dash component
    :rtype: dash.development.base_component.ComponentMeta
    """
    return html.Div([
        html.Div(id='live-screen'),
        dcc.Interval(
            id='screen-interval-component', interval=1000, n_intervals=0),
        html.Div([
            dcc.Input(id='native-key-control', type='text', value=''),
        ],
                 style={'margin': style.PADDING}),
        html.Button(
            id='native-key-control-button',
            n_clicks=0,
            children='Execute',
            style={
                'margin': style.PADDING,
                'backgroundColor': style.BUTTON_COLOR
            })
    ], style={'margin': style.PADDING})
