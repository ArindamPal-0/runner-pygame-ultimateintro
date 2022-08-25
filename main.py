import pygame
from sys import exit
from random import randint

def display_score(start_time: int, test_font: pygame.font.Font, screen: pygame.Surface) -> int:
    """Calculating and displaying current score on the screen"""
    # get the curren time as ticks
    current_time = ((pygame.time.get_ticks() // 1000) - start_time)

    # creating the score surface with the current time tick
    score_surface = test_font.render(f'Score: {current_time}', False,  (64, 64, 64))
    # getting the score rect and positioning it
    score_rect = score_surface.get_rect(center = (400, 50))
    # rendering the score surface on the screen
    screen.blit(score_surface, score_rect)

    return current_time

def obstacle_movement(obstacle_list: list[pygame.Rect], snail_surface: pygame.Surface, fly_surface: pygame.Surface, screen: pygame.Surface) -> None:
    """Handling obstacle movement and their removal on exiting screen space"""
    for index, obstacle_rect in enumerate(obstacle_list):
        obstacle_rect.x -= 5

        # drawing appropriate obstacle
        if obstacle_rect.bottom == 300:
            screen.blit(snail_surface, obstacle_rect)
        else:
            screen.blit(fly_surface, obstacle_rect)

        if obstacle_rect.bottomright[0] < 0:
            obstacle_list.remove(obstacle_rect)

def collisions(player: pygame.Rect, obstacles: list[pygame.Rect]) -> bool:
    """Checks for collisions and returns True if any collision found, otherwise False."""
    for obstacle_rect in obstacles:
        if player.colliderect(obstacle_rect):
            return True
    return False

def player_animation(player_rect: pygame.Rect, player_index: float, player_walk: list[pygame.Surface], player_jump: pygame.Surface) -> tuple[float, pygame.Surface]:
    """Player walking animation walk, jump and their transition."""

    player_surface: pygame.Surface = None

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
    
    return player_index, player_surface

# main function
def main() -> int:
    """Main function which runs when the program is executed, returns 0 if exits successfully"""

    # very important to initialize the pygame module
    pygame.init()

    # creating a display surface
    screen: pygame.Surface = pygame.display.set_mode((800, 400))
    # set window title
    pygame.display.set_caption("Runner")

    clock = pygame.time.Clock()

    game_active: bool = False

    start_time: int = 0

    score: int = 0

    # font
    test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

    sky_surface: pygame.Surface = pygame.image.load('graphics/Sky.png').convert()
    ground_surface: pygame.Surface = pygame.image.load('graphics/ground.png').convert()

    # score_surface: pygame.Surface = test_font.render('My game', False, (64, 64, 64))
    # score_rect: pygame.Rect = score_surface.get_rect(center=(400, 50))

    # Obstacles

    # Snail
    snail_frame_1: pygame.Surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
    snail_frame_2: pygame.Surface = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
    snail_frames: list[pygame.Surface] = [snail_frame_1, snail_frame_2]
    snail_frame_index: float = 0
    snail_surface: pygame.Surface = snail_frames[snail_frame_index]

    # Fly
    fly_frame_1: pygame.Suface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
    fly_frame_2: pygame.Suface = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
    fly_frames: list[pygame.Surface] = [fly_frame_1, fly_frame_2]
    fly_frame_index: float = 0
    fly_surface: pygame.Surface = fly_frames[fly_frame_index]

    obstacle_rect_list: list[pygame.Rect] = []

    player_walk_1: pygame.Surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
    player_walk_2: pygame.Surface = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
    player_walk: list[pygame.Surface] = [player_walk_1, player_walk_2]
    player_index: float = 0
    player_jump: pygame.Surface = pygame.image.load('graphics/player/jump.png').convert_alpha()

    player_surface: pygame.Surface = player_walk[int(player_index)]
    player_rect: pygame.Rect = player_surface.get_rect(midbottom=(80, 300))

    player_gravity: int = 0

    # Intro screen
    # importing the image
    player_stand: pygame.Surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
    # scale the image surface
    # player_stand = pygame.transform.scale2x(player_stand)
    player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
    player_stand_rect: pygame.Rect = player_stand.get_rect(center = (400, 200))

    game_name: pygame.Surface = test_font.render("Pixel Runner", False, (111, 196, 169))
    game_name_rect: pygame.Rect = game_name.get_rect(center = (400, 80))

    game_message: pygame.Surface = test_font.render('Press space to run', False, (111, 196, 169))
    game_message_rect: pygame.Rect = game_message.get_rect(center = (400, 340))


    # Timer
    obstacle_timer: int = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1500)

    snail_animation_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(snail_animation_timer, 400)

    fly_animation_timer = pygame.USEREVENT + 3
    pygame.time.set_timer(fly_animation_timer, 200)

    while True:
        # draw all our elements
        # update everything

        # check for events
        for event in pygame.event.get():
            # checking of QUIT event
            if event.type == pygame.QUIT:
                # quiting pygame
                pygame.quit()
                # Returning from the main function and exiting
                return 0

            if game_active:
                # player jumps if we clicked on it
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # print(event.pos)
                    # only jump if player touching the ground
                    if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                        player_gravity = -20

                # player jumps if K_SPACE is pressed
                if event.type == pygame.KEYDOWN:
                    # only jump if player touching the ground
                    if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                        # print('jump')
                        player_gravity = -20
                
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = (pygame.time.get_ticks() // 1000)
            
            # run all timers if game is active
            if game_active:
                if event.type == obstacle_timer and game_active:
                    # adding obstacle whenever custom event is fired
                    if randint(0, 2):
                        obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 300)))
                    else:
                        obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 210)))
                
                if event.type == snail_animation_timer:
                    if snail_frame_index == 0:
                        snail_frame_index = 1
                    else:
                        snail_frame_index = 0
                    snail_surface = snail_frames[snail_frame_index]

                if event.type == fly_animation_timer:
                    if fly_frame_index == 0:
                        fly_frame_index = 1
                    else:
                        fly_frame_index = 0
                    fly_surface = fly_frames[fly_frame_index]

                

        if game_active:
            # block image transfer, display the image surface
            # draw order is important!
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))

            # draw score surface
            # pygame.draw.rect(screen, '#c0e8ec', score_rect, 20)
            # pygame.draw.rect(screen, '#c0e8ec', score_rect)
            # screen.blit(score_surface, score_rect)
            score = display_score(start_time, test_font, screen)

            # snail_rect.x -= 4
            # if snail_rect.right < 0:
            #     snail_rect.left = 800
            # screen.blit(snail_surface, snail_rect)

            # Player

            if player_rect.bottom > 300:
                player_rect.bottom = 300
                player_gravity = 0
            elif player_rect.bottom != 300 or player_gravity != 0:
                    player_gravity += 1
                    player_rect.bottom += player_gravity
            
            player_index, player_surface = player_animation(player_rect, player_index, player_walk, player_jump)
            screen.blit(player_surface, player_rect)

            # Obstacles movement

            obstacle_movement(obstacle_rect_list, snail_surface, fly_surface, screen)

            # collision

            game_active = not collisions(player_rect, obstacle_rect_list)

        
        else:
            screen.fill((94, 129, 162))
            screen.blit(player_stand, player_stand_rect)

            # removing all obstacles after game over
            obstacle_rect_list.clear()

            # resetting the player position
            player_rect.midbottom = (80, 300)
            player_gravity = 0

            score_message: pygame.Surface = test_font.render(f"Your score: {score}", False, (111, 196, 169))
            score_message_rect: pygame.Rect = score_message.get_rect(center = (400, 330))

            screen.blit(game_name, game_name_rect)

            if score == 0:
                screen.blit(game_message, game_message_rect)
            else:
                screen.blit(score_message, score_message_rect)

        # updates the created display surface
        pygame.display.update()




        # makes sure that the while loop doesn't run at more than 60 times per second
        clock.tick(60)
    
    return 1


if __name__ == '__main__':
    exit(main())