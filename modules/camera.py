#
#
#

import pygame.camera
import datetime


def initPygame():
    """initializes pygame if it has not been initialized yet"""
    if not pygame.get_init():
        pygame.init()
        pygame.camera.init()


def listCameras():
    """prints and returns a list of available cameras"""
    initPygame()
    print("Available Cameras:")
    cameras = pygame.camera.list_cameras()
    i = 0
    for camera in cameras:
        print('[', i, '] ', camera, sep='')
        i += 1

    return cameras


class Camera:
    """Class for attached cameras with automatic timestamping"""

    def __init__(self, deviceNum=0):
        initPygame()
        self.camera = pygame.camera.Camera(pygame.camera.list_cameras()[deviceNum])
        self.camera.start()
        print(self.camera.get_controls())
        self.width, self.height = self.camera.get_size()
        self.font = pygame.font.Font("../assets/fonts/Roboto_Mono/RobotoMono-Medium.ttf", 16)

    def getSize(self):
        return (self.width, self.height)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getImage(self, prefix='', suffix='', sep=' '):
        """Retrieves and timestamps an image from the camera.

        Gets an image from the initialized camera. Also gets the current time in the format m/d/Y H:M:S and combines it
        using the prefix, suffix, and sep keyword arguments. Renders the timestamp on to the image with a white
        background.

        Keyword Arguments:
            prefix (str): leading string of timestamp (default: '')
            suffix (str): trailing string of timestamp (default: '')
            sep (str): separator string between terms of time stamp (default: ' ')

        Returns:
            image (pygame.Surface): image with timestamp embedded
        """
        img = self.camera.get_image()
        text = prefix + sep + datetime.datetime.now().strftime('%m/%d/%Y' + sep + '%H:%M:%S') + sep + suffix
        stamp = self.font.render(text, True, (255, 0, 0))
        background = pygame.Surface((stamp.get_width() + 3, stamp.get_height() + 3))
        # background.set_alpha(128)
        background.fill((255, 255, 255))
        img.blit(background, (0, img.get_height() - background.get_height()))
        img.blit(stamp, (0, img.get_height() - stamp.get_height()))
        # TODO: create image class with built-in variables for remembering timestamp string and has methods for saving to the filesystem
        return img

    def stop(self):
        self.camera.stop()
        pygame.quit()


# Camera Module Test Script
if __name__ == '__main__':
    listCameras()
    webcam = Camera()

    # pygame window settings
    size = webcam.getSize()
    fps = 60
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    done = False

    # pygame main loop
    while not done:
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # draw routine
        screen.fill((20, 20, 20))
        img = webcam.getImage(prefix='yolo', suffix='turn around!')
        screen.blit(img, (0, 0))

        # update buffer
        pygame.display.flip()

        # cap FPS
        clock.tick(fps)

    # close the webcam (will stop pygame)
    webcam.stop()
