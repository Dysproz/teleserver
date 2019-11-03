import cv2

from IoT_master.tools.secret_manager import SecretManager


class ThermalCamera:
    """This class initializes connection througth rtsp protocol with Dahua
    thermal ip camera based on the settings provided in .ini file.

    Ini file contains username, password, ip address and channel of the camera.

    URL format is:
    rtsp://username:password@ip:port/cam/realmonitor?channel=1&subtype=0

    There are only 2 channels, '1': normal vision and '2': thermal vision.
    """
    def __init__(self, file=None):
        """Initializes class and reads settings from .ini file.

        :param file: path and name of the .ini file
        :type file: str
        """
        if file:
            sec = SecretManager(secret_file=file)
        else:
            sec = SecretManager()
        config = sec.thermal_camera_credentials()
        self.login = config['login']
        self.password = config['password']
        self.ip_address = config['ip_address']
        self.channel = config['channel']
        self.address = (f'rtsp://{self.login}:{self.password}@{self.ip_address}'
                        f'/cam/realmonitor?channel={self.channel}&subtype=0')
        self.cam = cv2.VideoCapture(self.address)

    def change_channel(self, new_channel):
        """This function gives easy way to change channel which gives feed
        to progam.

        :param new_channel: Which channel you want to change into
        :type new_channel: str
        """
        self.channel = new_channel
        self.address = (f'rtsp://{self.login}:{self.password}@{self.ip_address}'
                        f'/cam/realmonitor?channel={self.channel}&subtype=0')
        self.cam = cv2.VideoCapture(self.address)

    def get_picture(self):
        """Function used to get picture from the camera.

        :return ret: Check if reading from camera is successful
        :rtype ret: boolean
        :return img: Read image from camera
        :rtype img: numpy.ndarray
        """
        self.ret, self.img = self.cam.read()
        return self.ret, self.img


if __name__ == '__main__':
    """This part of the code only runs when script is run as main module
    and doesn't run when it is imported module.

    Initializes ThermalCamera class and displays image from camera in window.
    Two working keys are ESC to close window and SPACE to change displayed channel.
    """

    camera_class = ThermalCamera()
    cv2.namedWindow('Camera')
    channels = ['1', '2']
    i = 0

    while True:
        ret, img = camera_class.get_picture()
        print(type(img))
        if not ret:
            break
        cv2.imshow('Camera', img)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            camera_class.change_channel(channels[i % 2])
            i = i+1
    camera_class.cam.release()
    cv2.destroyAllWindows
