import dash_html_components as html
import dash_core_components as dcc
import tools.system_calls as system


PADDING = '10px'
BUTTON_COLOR = '#d3d3d3'


def gui_layout():
    layout = html.Div([
        html.H1(children='teleserver', style={'font-family': 'helvetica',
                                              'color': '#3B5DBC',
                                              'font-size': '50',
                                              'text-align': 'center',
                                              'vertical-align': 'text-top'}),
        # URL section
        html.Div([
            dcc.Input(
                id='url',
                type='text',
                value=''
            ),
        ]),
        html.Div([
            html.Button(id='url-button',
                        n_clicks=0,
                        children='Cast',
                        style={'margin': PADDING,
                               'backgroundColor': BUTTON_COLOR}),

            html.Button(id='url-close-button',
                        n_clicks=0,
                        children='Close',
                        style={'margin': PADDING,
                               'backgroundColor': BUTTON_COLOR})
        ]),

        # Screenshot, reboot, poweroff section
        html.Div([
            html.Button(id='screenshot-button',
                        n_clicks=0,
                        children='Screenshot',
                        style={'display': 'inline-block',
                               'text-align': 'center',
                               'margin': PADDING,
                               'backgroundColor': BUTTON_COLOR}),

            html.Button(id='reboot-button',
                        n_clicks=0,
                        children='Reboot',
                        style={'display': 'inline-block',
                               'text-align': 'center',
                               'margin': PADDING,
                               'backgroundColor': BUTTON_COLOR}),

            html.Button(id='poweroff-button',
                        n_clicks=0,
                        children='Power Off',
                        style={'display': 'inline-block',
                               'text-align': 'center',
                               'margin': PADDING,
                               'backgroundColor': BUTTON_COLOR})
        ]),

        # Volume section
        html.Div([
            html.Div([dcc.Slider(
                id='volume-slider',
                min=0,
                max=100,
                step=1,
                value=system.get_volume()
            )], style={'width': '50%',
                       'display': 'inline-block',
                       'padding': PADDING}),

            html.Div(id='volume-indicator', style={'padding': PADDING}),

            html.Button(id='set-volume-button',
                        n_clicks=0,
                        children='Set Volume',
                        style={'margin': PADDING,
                               'backgroundColor': BUTTON_COLOR}),

            html.Button(id='mute-button',
                        n_clicks=0,
                        children='Mute',
                        style={'margin': PADDING,
                               'backgroundColor': BUTTON_COLOR})
        ]),

        # Tabs
        html.Div([
            dcc.Tabs(id="tabs", value='upload-tab', children=[
                dcc.Tab(label='Upload', value='upload-tab'),
                ]),
            html.Div(id='tabs-content')
        ]),

        # Dummy outputs section
        html.Div([
            html.Div(id='open-output-message')
        ], style={'display': 'none'}),
        html.Div([
            html.Div(id='close-output-message')
        ], style={'display': 'none'}),
        html.Div([
            html.Div(id='screenshot-output-message')
        ], style={'display': 'none'}),
        html.Div([
            html.Div(id='reboot-output-message')
        ], style={'display': 'none'}),
        html.Div([
            html.Div(id='poweroff-output-message')
        ], style={'display': 'none'}),
        html.Div([
            html.Div(id='mute-output-message')
        ], style={'display': 'none'})
    ], style={'text-align': 'center',
              'font-family': 'helvetica',
              'position': 'absolute',
              'top': '0',
              'left': '0',
              'width': '100%',
              'height': '100%',
              'backgroundColor': '#66BDDC'})

    return layout


def create_upload_content():
    output = html.Div([
        html.H1("File Browser"),
        html.H2("Upload"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ), style={"width": "100%",
                      "height": "60px",
                      "lineHeight": "60px",
                      "borderWidth": "1px",
                      "borderStyle": "dashed",
                      "borderRadius": "5px",
                      "textAlign": "center",
                      "margin": "10px",
                      },
            multiple=True,
        ),
        html.H2("File List"),
        html.Ul(id="file-list"),
    ], style={'font-family': 'helvetica',
              'color': ' #525252',
              'font-size': '20',
              'text-align': 'center',
              'vertical-align': 'text-top',
              'max-width': '50%',
              'display': 'inline-block'})
    return output


def tab_render(tab):
    if tab == 'upload-tab':
        return create_upload_content()
