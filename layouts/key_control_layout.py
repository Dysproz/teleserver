import dash_core_components as dcc
import dash_html_components as html

import layouts.style.style as style

web_key_shortcuts = [('Next tab', 'ctrl+Tab'),
                     ('Previous tab', 'ctrl+shift+Tab'),
                     ('Previous page', 'alt+Left'), ('Next page', 'alt+Right'),
                     ('Close current tab', 'ctrl+w')]

system_key_shortcuts = [('Switch Application', 'Super+Tab'),
                        ('Minimalize', 'Super+h'), ('Maximalize', 'Super+Up'),
                        ('View Split Left', 'Super+Left'),
                        ('View Split Right', 'Super+Right'),
                        ('Zoom in', 'Alt+Super+='), ('Zoom out',
                                                     'Alt+Super+-')]

SHORTCUT_NAMES = [
    '{}-button'.format(key)
    for _, key in web_key_shortcuts + system_key_shortcuts
]

SHORTCUTS = web_key_shortcuts + system_key_shortcuts


def create_key_control_layout():
    """Create dash key control tab layout

    :return: Key control tab layout as dash component
    :type: dash.development.base_component.ComponentMeta
    """
    return html.Div([
        html.Div([
            dcc.Input(id='key-control', type='text', value=''),
        ],
                 style={'margin': style.PADDING}),
        html.Button(
            id='key-control-button',
            n_clicks=0,
            children='Execute',
            style={
                'margin': style.PADDING,
                'backgroundColor': style.BUTTON_COLOR
            }),
        create_sample_key_shortcuts()
    ])


def create_sample_key_shortcuts():
    """Create dash layout form key shortcuts layout

    :return: Dash component with key shortcuts
    :type: dash.development.base_component.ComponentMeta
    """
    web_buttons = []
    [
        web_buttons.append(
            html.Button(
                id='{}-button'.format(key),
                n_clicks_timestamp=0,
                children=command,
                style={
                    'margin': style.PADDING,
                    'backgroundColor': style.BUTTON_COLOR
                })) for command, key in web_key_shortcuts
    ]

    system_buttons = []
    [
        system_buttons.append(
            html.Button(
                id='{}-button'.format(key),
                n_clicks_timestamp=0,
                children=command,
                style={
                    'margin': style.PADDING,
                    'backgroundColor': style.BUTTON_COLOR
                })) for command, key in system_key_shortcuts
    ]

    return html.Div([
        html.H3(children='Web Shortcuts'),
        html.Div(web_buttons),
        html.H3(children='System Shortcuts'),
        html.Div(system_buttons)
    ])
