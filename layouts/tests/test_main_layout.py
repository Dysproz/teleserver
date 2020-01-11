import dash
import os
from pathlib import Path
from pyfakefs import fake_filesystem_unittest
from unittest.mock import patch
import yaml

from layouts.main_layout import gui_layout, tab_render
from tools.common import UPLOAD_DIRECTORY, TELESERVER_DIR


class TestMainLayout(fake_filesystem_unittest.TestCase):

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_dir = Path(dir_path).parent.parent
        with open(f'{config_dir}/config.yml', 'r') as config_file:
            config_data = yaml.safe_load(config_file)
        self.setUpPyfakefs()
        os.makedirs(f'{TELESERVER_DIR}/app')
        with open(f'{TELESERVER_DIR}/app/config.yml', 'w') as config_file:
            yaml.safe_dump(config_data, config_file, default_flow_style=False)

    def test_gui_layout(self):
        self.assertIsInstance(type(gui_layout()),
                              dash.development.base_component.ComponentMeta)

    def test_tab_render_upload_tab(self):
        os.makedirs(UPLOAD_DIRECTORY)
        os.mknod(f'{UPLOAD_DIRECTORY}/a.txt')
        os.mknod(f'{UPLOAD_DIRECTORY}/b.txt')
        os.mknod(f'{UPLOAD_DIRECTORY}/c.txt')
        self.assertIsInstance(type(tab_render('upload-tab')),
                              dash.development.base_component.ComponentMeta)

    @patch('alsaaudio.Mixer')
    def test_tab_render_system_options_tab(self, mixer):
        self.assertIsInstance(type(tab_render('system-options-tab')),
                              dash.development.base_component.ComponentMeta)

    def test_tab_render_shortcuts_tab(self):
        self.assertIsInstance(type(tab_render('shortcuts-tab')),
                              dash.development.base_component.ComponentMeta)

    def test_tab_render_keyboard_tab(self):
        self.assertIsInstance(type(tab_render('keyboard-tab')),
                              dash.development.base_component.ComponentMeta)

    def test_tab_render_screen_tab(self):
        self.assertIsInstance(type(tab_render('screen-tab')),
                              dash.development.base_component.ComponentMeta)
