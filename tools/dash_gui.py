import dash_html_components as html
import dash_core_components as dcc
import tools.system_calls as system
import tools.app_callbacks as callback

PADDING = '10px'
BUTTON_COLOR = '#d3d3d3'


def gui_layout():
    layout = html.Div([html.Div([
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

        # Tabs
        html.Div([
            dcc.Tabs(id="tabs", value='system-options-tab', children=[
                dcc.Tab(label='System Options', value='system-options-tab'),
                dcc.Tab(label='Files', value='upload-tab'),
                dcc.Tab(label='Screen', value='screen-tab')
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
        ], style={'display': 'none'}),
    ], style={'text-align': 'center',
              'font-family': 'helvetica',
              'position': 'absolute',
              'top': '0',
              'left': '0',
              'width': '100%',
              'height': '100%',
              'backgroundColor': '#FFFFFF'}),
    html.A([
            html.Img(
                src='https://raw.githubusercontent.com/Dysproz/teleserver/master/images/info.png',
                style={
                    'height' : '1.2%',
                    'width' : '1.2%',
                    'float' : 'right',
                    'position' : 'relative',
                    'padding-top' : 0,
                    'padding-right' : 0
                })
    ], href='https://github.com/Dysproz/teleserver')

    ])
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
        dcc.Checklist(
            id='files-checklist',
            options=callback.get_files_list(),
            values=[]
    ),
    html.Div(id='output-data-upload'),
    html.Div([
        html.Button(id='download-files-button',
                    n_clicks=0,
                    children='Download',
                    style={'margin': PADDING,
                           'backgroundColor': BUTTON_COLOR}),
        html.Button(id='delete-files-button',
                    n_clicks=0,
                    children='Delete',
                    style={'margin': PADDING,
                           'backgroundColor': BUTTON_COLOR}),
        html.Button(id='open-files-button',
                    n_clicks=0,
                    children='Open',
                    style={'margin': PADDING,
                           'backgroundColor': BUTTON_COLOR})
    ])
    ], style={'font-family': 'helvetica',
              'color': ' #525252',
              'font-size': '20',
              'text-align': 'center',
              'vertical-align': 'text-top',
              'max-width': '50%',
              'display': 'inline-block'})
    return output


def create_system_options():
    return html.Div([
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

                    html.Div(id='volume-indicator',
                             style={'padding': PADDING}),

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
                # Screenshot, reboot, poweroff section
                html.Div([
                    html.Button(id='screenshot-button',
                                n_clicks=0,
                                children='Screenshot',
                                style={'text-align': 'center',
                                       'margin': PADDING,
                                       'backgroundColor': BUTTON_COLOR}),
                ]),
                html.Div([
                    html.Button(id='reboot-button',
                                n_clicks=0,
                                children='Reboot',
                                style={'text-align': 'center',
                                       'margin': PADDING,
                                       'backgroundColor': BUTTON_COLOR}),

                    html.Button(id='poweroff-button',
                                n_clicks=0,
                                children='Power Off',
                                style={'text-align': 'center',
                                       'margin': PADDING,
                                       'backgroundColor': BUTTON_COLOR})
                ])
            ])


def create_screen_content():
    return html.Div([
        html.Div(id='live-screen'),
        dcc.Interval(
            id='screen-interval-component',
            interval=1000,
            n_intervals=0
        )
    ])


def tab_render(tab):
    if tab == 'upload-tab':
        return create_upload_content()
    elif tab == 'system-options-tab':
        return create_system_options()
    elif tab == 'screen-tab':
        return create_screen_content()


def files_tab_render(tab,
                     uploaded_filenames,
                     uploaded_file_contents):
    if tab == 'download-tab':
        return callback.create_download_files_content(uploaded_filenames,
                                                      uploaded_file_contents)
    elif tab == 'delete-tab':
        return callback.create_delete_files_content(uploaded_filenames,
                                                    uploaded_file_contents)
