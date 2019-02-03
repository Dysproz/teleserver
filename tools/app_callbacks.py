import base64
import os
from urllib.parse import quote as urlquote
import dash_html_components as html
import tools.system_calls as system
import flask


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


def upload(uploaded_filenames, uploaded_file_contents):
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)


def get_files_list():
    files = uploaded_files()
    return [{'label': filename, 'value': filename} for filename in files]


def download_files(files, server, UPLOAD_DIRECTORY=UPLOAD_DIRECTORY):
    for filename in files:
        flask.send_from_directory(UPLOAD_DIRECTORY,
                                   filename,
                                   as_attachment=True)


def delete_files(files, UPLOAD_DIRECTORY=UPLOAD_DIRECTORY):
    for filename in files:
        os.remove('{dir}/{filename}'.format(dir=UPLOAD_DIRECTORY,
                                            filename=filename))


def open_files(files, UPLOAD_DIRECTORY=UPLOAD_DIRECTORY):
    for filename in files:
        system.web_open('file://{dir}/{filename}'.format(dir=UPLOAD_DIRECTORY,
                                                         filename=filename))


def get_screen_grab():
    return html.Img(src='data:image/jpeg;base64,{}'
                        .format(system.get_screen()),
                    style={'width': '75%', 'height': '75%'})
