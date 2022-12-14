import pygame, pygame.camera


width, height = size = (640,320)
fps = 30

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

pygame.camera.init()
cameras = pygame.camera.list_cameras()
print(cameras)
webcam = pygame.camera.Camera(cameras[0])
webcam.start()



while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    img = webcam.get_image()
    screen.fill((0,0,0))
    screen.blit(img,(0,0))
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()