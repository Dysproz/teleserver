import dash_core_components as dcc
import dash_html_components as html
import layouts.style.style as style
from tools.app_callbacks import get_files_list


def create_upload_content():
    """Dash html layout of Files tab

    :return: Files tab layout as dash component
    :rtype: dash.development.base_component.ComponentMeta
    """
    output = html.Div(
        [
            html.H1("File Browser"),
            html.H2("Upload"),
            dcc.Upload(
                id="upload-data",
                children=html.Div(
                    ["Drag and drop or click to select a file to upload."]),
                style={
                    "width": "100%",
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
                options=get_files_list(),
                values=[]),
            html.Div(id='output-data-upload'),
            html.Div([
                html.Button(
                    id='download-files-button',
                    n_clicks=0,
                    children='Prepare Download',
                    style={
                        'margin': style.PADDING,
                        'backgroundColor': style.BUTTON_COLOR
                    }),
                html.Button(
                    id='delete-files-button',
                    n_clicks=0,
                    children='Delete',
                    style={
                        'margin': style.PADDING,
                        'backgroundColor': style.BUTTON_COLOR
                    }),
                html.Button(
                    id='open-files-button',
                    n_clicks=0,
                    children='Open',
                    style={
                        'margin': style.PADDING,
                        'backgroundColor': style.BUTTON_COLOR
                    }),
            ]),
            html.Div([html.A('Download link', href='/download')])
        ],
        style={
            'margin': style.PADDING,
            'font-family': 'helvetica',
            'color': ' #525252',
            'font-size': '20',
            'text-align': 'center',
            'vertical-align': 'text-top',
            'max-width': '50%',
            'display': 'inline-block'
        })
    return output
