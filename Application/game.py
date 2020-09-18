import pygame, os

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (690, 50)  # Game window position

# Color definition
white = (255, 255, 255)
black = (0, 0, 0)

# Screen Setup
display_width = 540  # 9:16 Screen aspect ratio
display_height = 960
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Player Ship
player_ship_pos_x = (display_width * 0.45)
player_ship_pos_y = (display_height * 0.8)
player_ship_image = pygame.image.load('../Assets/playerShip1_red.png')


def player_ship(x, y):
    screen.blit(player_ship_image, (round(x), round(y)))


# Game Loop
game_state = True
while game_state:
    # set background color
    screen.fill(black)

    # draw player ship
    player_ship(player_ship_pos_x, player_ship_pos_y)

    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = False

    # screen refresh/update and performance
    pygame.display.update()
    frames_per_second = 45
    clock.tick(frames_per_second)

pygame.quit()  # stops pygame
quit()  # closes python
