"""A streamlined interface for generic cameras

A simplified way to connect and manage a integrated or USB camera via the pygame library. This also implements the
filters and automatically timestamps fetched images.

:authors: [RJLemker, Neko'z]
:date: December 14, 2022
:organization: UND Advanced Rocketry Club (ARC)
:version: 1.0
:status: in progress
"""

# Import Dependencies
import pygame.camera
import datetime
import os

# Global Variables and Constants
_CurrentConnections = []  # keeps track of all active cameras
_CameraStopsPygame = True  # stop pygame library when no cameras are connected
_Padding = 3  # spacing between font and background in pixels
_SavePath = '../data/'  # directory to save images relative to module
_Id = 0  # id numbers for name collision avoidance


# Camera Module Functions
def initPygame():
    """initializes pygame if it has not been initialized yet"""
    if not pygame.get_init():
        pygame.init()
        pygame.camera.init()


def listCameras():
    """prints and returns a list of available cameras

    :returns: list of camera names
    :rtype list[str]:
    """
    initPygame()

    print("Available Cameras:")
    cameras = pygame.camera.list_cameras()
    i = 0
    for camera in cameras:
        print('[', i, '] ', camera, sep='')
        i += 1

    return cameras


# Camera Module Classes
class Image(pygame.Surface):
    """a class that holds the image data fetched by the camera

    Will record the name and metadata captured by the

    :param surface: pygame image surface containing raw image
    :type surface: pygame.Surface
    """
    def __init__(self, surface):
        super().__init__(surface.get_size())
        self.blit(surface, (0, 0))
        self.name = ''
        global _Id
        self.id = _Id
        _Id += 1

    def setName(self, name):
        """Sets the filename

        :param name: the filename
        :type name: str
        """
        self.name = name

    def getName(self):
        """Gets the current filename attached to the image

        :returns: the filename
        :rtype str:
        """
        return self.name

    def save(self):
        """Saves the image to the filesystem

        Uses the save path variable and the attached filename to save the image data and metadata to the filesystem.
        """
        initPygame()
        pygame.image.save_extended(self, _SavePath + str(self.id) + '-' + self.name)
        # TODO: add metadata support


class Camera:
    """a class for attached cameras with automatic timestamping

    Will automatically connect to a connected camera (defaults to camera device id 0). Use getImage to take an image
    with various filters and have embedded timestamp with customizable text.

    :param device: the index of the camera from the available camera list
    :type device: int
    """
    def __init__(self, device=0):
        # initialize pygame library
        initPygame()

        # create pygame camera object
        self.camera = pygame.camera.Camera(pygame.camera.list_cameras()[device])

        # connect to camera
        self.start()

        # get size of camera images
        self.width, self.height = self.camera.get_size()

        # load timestamp font
        self.font = pygame.font.Font("../assets/fonts/Roboto_Mono/RobotoMono-Medium.ttf", 16)

    def start(self):
        """connect to camera

        Automatically connects upon object initialization.
        """
        # check if camera is already started
        if self not in _CurrentConnections:
            self.camera.start()  # start camera
            _CurrentConnections.append(self)  # add camera to current connections list

    def getSize(self):
        """returns the size of the image the camera captures

        :returns: a tuple containing a pair values containing the width and height
        :rtype Tuple[int, int]:
        """
        return self.width, self.height

    def getWidth(self):
        """returns the width of the image the camera captures

        :returns: width of the image the camera captures in pixels
        :rtype int:
        """
        return self.width

    def getHeight(self):
        """Returns the height of the image the camera captures

        :returns: height of the image the camera captures in pixels
        :rtype int:
        """
        return self.height

    def getImage(self, prefix='', suffix='', sep=' '):
        """retrieves and timestamps an image from the camera

        Gets an image from the initialized camera. Also gets the current time in the format m/d/Y H:M:S and combines
        it using the prefix, suffix, and sep keyword arguments. Renders the timestamp on to the image with a white
        background. Timestamp will be in lower left corner of image.

        :param prefix: leading string of timestamp
        :type prefix: str
        :param suffix: trailing string of timestamp
        :type suffix: str
        :param sep: separator string between terms of time stamp
        :type sep: str
        :returns: image with embedded timestamp
        :rtype Surface:
        """
        # get image from camera
        image = Image(self.camera.get_image())

        # create timestamp string
        text = ''
        if len(prefix) > 0:
            text += prefix + sep
        text += datetime.datetime.now().strftime('%m/%d/%Y' + sep + '%H:%M:%S')
        if len(suffix) > 0:
            text += sep + suffix

        # use timestamp to generate name
        special = {'/': '-', ':': '-', ' ': '_'}  # mapping from characters used in filesystem to acceptable alternative
        for letter in text:
            if letter in special:
                letter = special[letter]
            image.name += letter
        image.name += '.jpg'

        # render timestamp string into an graphic
        stamp = self.font.render(text, True, (255, 0, 0))

        # create a background image slightly bigger then the timestamp graphic
        background = pygame.Surface(
            (stamp.get_width() + _Padding * 2, stamp.get_height() + _Padding * 2))  # set background size
        # background.set_alpha(128)  # set background transparency
        background.fill((255, 255, 255))  # set background color

        # draw the background onto the camera graphic
        image.blit(background, (0, image.get_height() - background.get_height()))

        # draw the timestamp onto the camera image
        image.blit(stamp, (_Padding, image.get_height() - stamp.get_height() - _Padding))

        return image

    def stop(self):
        """closes the connection to the camera and stops pygame"""
        self.camera.stop()

        _CurrentConnections.remove(self)  # remove camera from active connection list
        if len(_CurrentConnections) == 0 and _CameraStopsPygame:
            pygame.quit()  # close pygame if no cameras are active


# Camera Module Test Script
if __name__ == '__main__':
    # list all camera devices
    listCameras()

    # connect to the first camera
    cam = Camera()

    # start pygame
    pygame.init()  # not necessary since camera will do this

    # pygame window settings
    size = cam.getSize()  # set size of GUI window
    fps = 60  # set max FPS of window
    screen = pygame.display.set_mode(size)  # create window
    pygame.display.set_caption("Camera Test")  # set title of window
    # set window icon
    icon = pygame.image.load("../assets/images/CameraIcon.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()  # create clock to track frame rate
    done = False
    latestImage = None

    # disable the camera from stopping pygame
    _CameraStopsPygame = False

    # pygame main loop
    while not done:
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_SPACE:
                    if latestImage != None:
                        latestImage.save()

        # draw routine
        screen.fill((20, 20, 20))
        latestImage = cam.getImage(prefix='example', suffix='ABC')
        screen.blit(latestImage, (0, 0))

        # update buffer
        pygame.display.flip()

        # cap FPS
        clock.tick(fps)

    # close the camera (will stop pygame)
    cam.stop()
    pygame.quit()
