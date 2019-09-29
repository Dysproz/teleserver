import dash
import os

from pyfakefs import fake_filesystem_unittest

from layouts.files_layout import create_upload_content
from tools.common import UPLOAD_DIRECTORY


class TestFilesLayout(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_create_upload_content(self):
        os.makedirs(UPLOAD_DIRECTORY)
        os.mknod(f'{UPLOAD_DIRECTORY}/a.txt')
        os.mknod(f'{UPLOAD_DIRECTORY}/b.txt')
        os.mknod(f'{UPLOAD_DIRECTORY}/c.txt')
        self.assertIsInstance(type(create_upload_content()),
                              dash.development.base_component.ComponentMeta)
