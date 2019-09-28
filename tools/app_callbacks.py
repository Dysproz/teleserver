import base64
import dash_html_components as html
import flask
import os
from subprocess import call
import zipfile

import tools.system_calls as system


UPLOAD_DIRECTORY = str(os.path.join(os.getcwd(), 'app_uploaded_files'))


def create_upload_directory():
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    call(['gsettings',
          'set',
          'org.gnome.gnome-screenshot',
          'auto-save-directory',
          'file://{}'.format(UPLOAD_DIRECTORY)])


def save_file(name, content):
    """Save file to the machine

    :param name: Name of the file
    :type name: str
    :param content: Content of the file
    :type content: base64.bytes
    """
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """Get list of the files in teleserver upload directory

    :return: List of files
    :rtype: list
    """
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def upload(uploaded_filenames, uploaded_file_contents):
    """Upload multiple files

    :param uploaded_filenames: Filenames of files
    :type uploaded_filenames: list
    :param uploaded_file_contents: Content of files
    :type uploaded_file_contents: list
    """
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)


def get_files_list():
    """Get list of uploaded files

    :return: List of files
    :rtype: list
    """
    files = uploaded_files()
    return [{'label': filename, 'value': filename} for filename in files]


def download_files(files):
    """Download selected files

    :param files: List fo files to download
    :type files: list
    """
    zipf = zipfile.ZipFile('teleserver_download.zip', 'w',
                           zipfile.ZIP_DEFLATED)
    for filename in files:
        zipf.write(
            '{dir}/{filename}'.format(dir=UPLOAD_DIRECTORY, filename=filename),
            arcname=filename)
    zipf.close()
    flask.send_file(
        'teleserver_download.zip',
        mimetype='zip',
        attachment_filename='teleserver_download.zip',
        as_attachment=True)


def delete_files(files):
    """Delete selected files

    :param files: List fo files to delete
    :type files: list
    """
    for filename in files:
        os.remove('{dir}/{filename}'.format(
            dir=UPLOAD_DIRECTORY, filename=filename))


def open_files(files):
    """Open selected files

    :param files: Files to open
    :type files: list
    """
    for filename in files:
        system.web_open('file://{dir}/{filename}'.format(
            dir=UPLOAD_DIRECTORY, filename=filename))


def get_screen_grab():
    """Get dash html Img object of teleserver current screen

    :return: Screen snapshot as dash component
    :rtype: dash.development.base_component.ComponentMeta
    """
    return html.Img(
        src='data:image/jpeg;base64,{}'.format(system.get_screen()),
        style={
            'width': '75%',
            'height': '75%'
        })
