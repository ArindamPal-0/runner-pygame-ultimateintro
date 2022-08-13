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

sky_surface: pygame.Surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface: pygame.Surface = pygame.image.load('graphics/ground.png').convert()
text_surface: pygame.Surface = test_font.render('My game', False, 'Black')

snail_surface: pygame.Surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect: pygame.Rect = snail_surface.get_rect(midbottom=(600, 300))

player_surface: pygame.Surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect: pygame.Rect = player_surface.get_rect(midbottom=(80, 300))

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

        if event.type == pygame.MOUSEMOTION:
            # print(event.pos)

            # check if the mouse is over the player rectangle
            if player_rect.collidepoint(event.pos):
                print('mouse over player')

        if event.type == pygame.MOUSEBUTTONDOWN:
            print('mouse down')

        if event.type == pygame.MOUSEBUTTONUP:
            print('mouse up')

    # block image transfer, display the image surface
    # draw order is important!
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (300, 50))

    snail_rect.x -= 4
    if snail_rect.right < 0:
        snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)

    player_rect.left += 1
    screen.blit(player_surface, player_rect)

    # collision check
    # if player_rect.colliderect(snail_rect):
    #     print('collision')

    # collision of a point (mouse pos) with rectangle (player)
    mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint(mouse_pos):
        # print('collision')
        if pygame.mouse.get_pressed()[0]:
            print('pressed')

    # updates the created display surface
    pygame.display.update()

    # makes sure that the while loop doesn't run at more than 60 times per second
    clock.tick(60)