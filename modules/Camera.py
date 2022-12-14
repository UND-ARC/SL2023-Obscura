import pygame.camera
import datetime

class Camera:
    def __init__(self, deviceNum=0):
        pygame.init()
        pygame.camera.init()
        self.camera = pygame.camera.Camera(pygame.camera.list_cameras()[deviceNum])
        self.camera.start()
        self.width, self.height = self.camera.get_size()
        print(pygame.font.get_fonts())
        self.font = pygame.font.Font("../assets/fonts/Roboto_Mono/RobotoMono-Medium.ttf", 16)
        #    .SysFont('comicsansms', 24)

    def listCameras(self):
        print("Available Cameras:")
        cameras = pygame.camera.list_cameras()
        i = 0
        for camera in cameras:
            print('[', i, '] ', camera, sep='')

        return cameras

    def getSize(self):
        return (self.width, self.height)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getImage(self, prefix='', suffix='', sep=' '):
        img = self.camera.get_image()
        text = prefix + sep + datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S') + sep + suffix
        stamp = self.font.render(text, True, (255, 0, 0))
        background = pygame.Surface((stamp.get_width() + 3, stamp.get_height() + 3))
        #background.set_alpha(128)
        background.fill((255, 255, 255))
        img.blit(background, (0, img.get_height() - background.get_height()))
        img.blit(stamp, (0, img.get_height() - stamp.get_height()))
        return img

    def stop(self):
        self.camera.stop()
        pygame.quit()

### Camera Module Test Script
if __name__ == '__main__':
    webcam = Camera()
    webcam.listCameras()

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

    webcam.stop()