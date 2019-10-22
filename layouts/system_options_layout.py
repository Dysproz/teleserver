import dash_core_components as dcc
import dash_html_components as html
import layouts.style.style as style
import tools.system_calls as system


def create_system_options():
    """Create layout for system options tab

    :return: System options layout as dash component
    :rtype: dash.development.base_component.ComponentMeta
    """
    return html.Div([
        # Volume section
        html.Div([
            html.Div([
                dcc.Slider(
                    id='volume-slider',
                    min=0,
                    max=100,
                    step=1,
                    value=system.get_volume())
            ],
                     style={
                         'margin': style.PADDING,
                         'width': '50%',
                         'display': 'inline-block',
                         'padding': style.PADDING
                     }),
            html.Div(id='volume-indicator', style={'padding': style.PADDING}),
            html.Button(
                id='set-volume-button',
                n_clicks=0,
                children='Set Volume',
                style={
                    'margin': style.PADDING,
                    'backgroundColor': style.BUTTON_COLOR
                }),
            html.Button(
                id='mute-button',
                n_clicks=0,
                children='Mute',
                style={
                    'margin': style.PADDING,
                    'backgroundColor': style.BUTTON_COLOR
                })
        ]),
        # Screenshot, reboot, poweroff section
        html.Div([
            html.Button(
                id='screenshot-button',
                n_clicks=0,
                children='Screenshot',
                style={
                    'text-align': 'center',
                    'margin': style.PADDING,
                    'backgroundColor': style.BUTTON_COLOR
                }),
        ]),
        html.Div([
            html.Button(
                id='reboot-button',
                n_clicks=0,
                children='Reboot',
                style={
                    'text-align': 'center',
                    'margin': style.PADDING,
                    'backgroundColor': style.BUTTON_COLOR
                }),
            html.Button(
                id='poweroff-button',
                n_clicks=0,
                children='Power Off',
                style={
                    'text-align': 'center',
                    'margin': style.PADDING,
                    'backgroundColor': style.BUTTON_COLOR
                })
        ]),
        html.Button(
                id='service-principal-button',
                n_clicks=0,
                children='Generate Service Principal',
                style={
                    'text-align': 'center',
                    'margin': style.PADDING,
                    'backgroundColor': style.BUTTON_COLOR,
                    'float': 'bottom'
                }),
        html.Div(id='service-principal-output-message')
    ])
