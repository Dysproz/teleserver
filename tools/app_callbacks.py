import base64
import os
from urllib.parse import quote as urlquote
import dash_html_components as html
import tools.system_calls as system


UPLOAD_DIRECTORY = "/usr/local/teleserver/app_uploaded_files"


def create_upload_directory():
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)


def save_file(name, content):
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


def file_delete_link(filename):
    location = "/delete/{}".format(urlquote(filename))
    return html.A(filename, href=location)


def create_download_files_content(uploaded_filenames, uploaded_file_contents):
    # if uploaded_filenames is not None and uploaded_file_contents is not None:
    #         for name, data in zip(uploaded_filenames, uploaded_file_contents):
    #             save_file(name, data)
    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]


def create_delete_files_content(uploaded_filenames, uploaded_file_contents):
    if uploaded_filenames is not None and uploaded_file_contents is not None:
            for name, data in zip(uploaded_filenames, uploaded_file_contents):
                save_file(name, data)
    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_delete_link(filename)) for filename in files]


def get_files_list():
    files = uploaded_files()
    return [{'label': filename, 'value': filename} for filename in files]

def get_screen_grab():
    return html.Img(src='data:image/jpeg;base64,{}'
                        .format(system.get_screen()),
                    style={'width': '75%', 'height': '75%'})
