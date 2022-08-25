import pygame
from sys import exit
import random

class Player(pygame.sprite.Sprite):
    """Player class"""
    def __init__(self) -> None:
        super().__init__()

        player_walk_1: pygame.Surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2: pygame.Surface = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk: list[pygame.Surface] = [player_walk_1, player_walk_2]
        self.player_index: float = 0
        self.player_jump: pygame.Surface = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image: pygame.Surface = self.player_walk[self.player_index]
        self.rect: pygame.Rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity: int = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.01)

    def player_input(self) -> None:
        """Checking for player input for character movement."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self) -> None:
        """Applying gravity to the character, and checks for player above ground."""
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 300:
            self.rect.bottom = 300
        # elif self.player_rect.bottom != 300 or self.gravity != 0:
        #         self.gravity += 1
        #         self.player_rect.bottom += self.gravity

    def animation_state(self) -> None:
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self) -> None:
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def player_reset(self) -> None:
        self.rect.midbottom = (80, 300)
        self.gravity = 0

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        y_pos: int = 0
        if type == 'fly':
            fly_1: pygame.Surface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2: pygame.Surface = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames: list[pygame.Surface] = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1: pygame.Surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2: pygame.Surface = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames: list[pygame.Surface] = [snail_1, snail_2]
            y_pos = 300

        self.animation_index: int = 0

        self.image: pygame.Surface = self.frames[self.animation_index]
        self.rect: pygame.Rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))

    def animation_state(self) -> None:
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0

        self.image = self.frames[int(self.animation_index)]
    
    def update(self) -> None:
        self.animation_state()
        self.rect.x -= 6

    def destroy(self) -> None:
        if self.rect.x <= -100:
            self.kill()


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


def collision_sprite(player: pygame.sprite.GroupSingle, obstacle_group: pygame.sprite.Group) -> bool:
    # check if player collide with any obstacle
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        # reset the player pos
        player.sprite.player_reset()
        # remove all the obstacles
        obstacle_group.empty()
        return False
    return True


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

    # game active state
    game_active: bool = False

    start_time: int = 0

    # current score
    score: int = 0

    # background music
    bg_music = pygame.mixer.Sound("audio/music.wav")
    bg_music.set_volume(0.01)
    bg_music.play(loops=-1)

    # Groups
    player = pygame.sprite.GroupSingle()
    player.add(Player())

    obstacle_group = pygame.sprite.Group()

    # font
    test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

    sky_surface: pygame.Surface = pygame.image.load('graphics/Sky.png').convert()
    ground_surface: pygame.Surface = pygame.image.load('graphics/ground.png').convert()


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

            if not game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = (pygame.time.get_ticks() // 1000)
            
            # run all timers if game is active
            if game_active:
                if event.type == obstacle_timer and game_active:
                    # adding obstacle whenever custom event is fired
                    obstacle_group.add(Obstacle(random.choice(['fly', 'snail', 'snail', 'snail'])))
                

        if game_active:
            # draw sky and ground surface
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))

            # draw score surface
            score = display_score(start_time, test_font, screen)

            # draw and update player
            player.draw(screen)
            player.update()

            # draw and update obstacles
            obstacle_group.draw(screen)
            obstacle_group.update()

            # collision
            game_active = collision_sprite(player, obstacle_group)

        
        else:
            screen.fill((94, 129, 162))
            screen.blit(player_stand, player_stand_rect)

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