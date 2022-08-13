import pygame
from sys import exit

# very important to initialize the pygame module
pygame.init()

# creating a display surface
screen = pygame.display.set_mode((800, 400))
# set window title
pygame.display.set_caption("Runner")

clock = pygame.time.Clock()

# font
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')
text_surface = test_font.render('My game', False, 'Black')

while True:
    # draw all our elements
    # update everything

    # check for events
    for event in pygame.event.get():
        # checking of QUIT event
        if event.type == pygame.QUIT:
            # quiting pygame
            pygame.quit()
            # exiting the program
            exit()

    # block image transfer, display the image surface
    # draw order is important!
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (300, 50))

    # updates the created display surface
    pygame.display.update()

    # makes sure that the while loop doesn't run at more than 60 times per second
    clock.tick(60)