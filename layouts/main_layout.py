import dash_core_components as dcc
import dash_html_components as html

from layouts.calendar_layout import change_calendar_content
from layouts.files_layout import create_upload_content
from layouts.keyboard_layout import create_keyboard_layout
from layouts.key_control_layout import create_key_control_layout
from layouts.screen_layout import create_screen_content
import layouts.style.style as style
from layouts.system_options_layout import create_system_options


def gui_layout():
    """Create main layout for teleserver

    :return: GUI layout as dash component
    :rtype: dash.development.base_component.ComponentMeta
    """
    layout = html.Div([
        html.Div(
            [
                html.H1(
                    children='teleserver',
                    style={
                        'font-family': 'helvetica',
                        'color': '#3B5DBC',
                        'font-size': '50',
                        'text-align': 'center',
                        'vertical-align': 'text-top'
                    }),
                # URL section
                html.Div([
                    dcc.Input(id='url', type='text', value=''),
                ]),
                html.Div([
                    html.Button(
                        id='url-button',
                        n_clicks=0,
                        children='Cast',
                        style={
                            'margin': style.PADDING,
                            'backgroundColor': style.BUTTON_COLOR
                        }),
                    html.Button(
                        id='url-close-button',
                        n_clicks=0,
                        children='Close',
                        style={
                            'margin': style.PADDING,
                            'backgroundColor': style.BUTTON_COLOR
                        })
                ]),

                # Tabs
                html.Div([
                    dcc.Tabs(
                        id="tabs",
                        value='system-options-tab',
                        children=[
                            dcc.Tab(
                                label='System Options',
                                value='system-options-tab'),
                            dcc.Tab(label='Files', value='upload-tab'),
                            dcc.Tab(label='Shortcuts', value='shortcuts-tab'),
                            dcc.Tab(label='Keyboard', value='keyboard-tab'),
                            dcc.Tab(label='Screen', value='screen-tab'),
                            dcc.Tab(label='Calendar', value='calendar-tab')
                        ]),
                    html.Div(id='tabs-content')
                ]),

                # Dummy outputs section
                html.Div([html.Div(id='open-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='close-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='screenshot-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='reboot-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='poweroff-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='mute-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='download-files-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='delete-files-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='open-files-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='custom-shortcut-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='native-shortcut-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='shortcut-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='keyboard-output-message')],
                         style={'display': 'none'}),
                html.Div([html.Div(id='calendar-output-message')],
                         style={'display': 'none'})
            ],
            style={
                'text-align': 'center',
                'font-family': 'helvetica',
                'position': 'absolute',
                'top': '0',
                'left': '0',
                'width': '100%',
                'height': '100%',
                'backgroundColor': '#FFFFFF'
            }),
        html.A([
            html.Img(
                src='https://raw.githubusercontent.com/Dysproz'
                '/teleserver/master/images/info.png',
                style={
                    'height': '1.2%',
                    'width': '1.2%',
                    'float': 'right',
                    'position': 'relative',
                    'padding-top': 0,
                    'padding-right': 0
                })
        ],
               href='https://github.com/Dysproz/teleserver')
    ])
    return layout


def tab_render(tab):
    """Create render for tabs in main GUI

    :return: Rendered tabs as dash component
    :rtype: dash.development.base_component.ComponentMeta
    """
    if tab == 'upload-tab':
        return create_upload_content()
    elif tab == 'system-options-tab':
        return create_system_options()
    elif tab == 'shortcuts-tab':
        return create_key_control_layout()
    elif tab == 'keyboard-tab':
        return create_keyboard_layout()
    elif tab == 'screen-tab':
        return create_screen_content()
    elif tab == 'calendar-tab':
        return change_calendar_content()
