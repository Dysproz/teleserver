import os
from pyfakefs import fake_filesystem_unittest

from tools.camera_initialize import ThermalCamera
from tools.common import TELESERVER_DIR
from tools.secret_manager import SecretManager


class TestCameraInitialize(fake_filesystem_unittest.TestCase):

    login = 'test'
    password = 'secret'
    ip_address = '127.0.0.1'
    channel = '1'

    def setUp(self):
        self.setUpPyfakefs()
        os.makedirs(TELESERVER_DIR)
        sec = SecretManager()
        sec.create_secrets_for_thermal_camera(self.login,
                                              self.password,
                                              self.ip_address,
                                              self.channel)
        self.camera = ThermalCamera()

    def test_address_of_thermal_camera(self):
        proper_address = f'rtsp://{self.login}:{self.password}@{self.ip_address}'\
                         f'/cam/realmonitor?channel={self.channel}&subtype=0'
        self.assertEqual(self.camera.address, proper_address)

    def test_change_channel(self):
        self.channel = '0'
        proper_address = f'rtsp://{self.login}:{self.password}@{self.ip_address}'\
                         f'/cam/realmonitor?channel={self.channel}&subtype=0'
        self.camera.change_channel('0')
        self.assertEqual(self.camera.address, proper_address)
