import pygame, os, sys

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (690, 50)  # Game window position

# Game State
game_state = 1

# Color definition
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)

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


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        # Draws button surface on screen
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        # Draws text
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width // 2 - text.get_width() // 2),
                self.y + (self.height // 2 - text.get_height() // 2)))

    def mouse_over(self, pos):
        # pos is a tuple containing mouse position (x, y)
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


def game_menu():
    # Buttons
    play_button = Button(red, 100, 350, 350, 100, "Play")
    leaderboards_button = Button(red, 100, 550, 350, 100, "Leaderboards")

    while True:
        # set background color
        screen.fill(black)

        # Buttons draw
        play_button.draw(screen)
        leaderboards_button.draw(screen)

        # process events
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.mouse_over(pygame.mouse.get_pos()):
                    if event.button == 1:  # ensures left mouse click only
                        print("Play")
                        game_active()
                if leaderboards_button.mouse_over(pygame.mouse.get_pos()):
                    if event.button == 1:  # ensures left mouse click only
                        print("Leaderboards")

        # screen refresh/update and performance
        pygame.display.update()
        frames_per_second = 45
        clock.tick(frames_per_second)


def game_active():
    while True:
        # set background color
        screen.fill(black)

        # draw player ship
        player_ship(player_ship_pos_x, player_ship_pos_y)

        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # screen refresh/update and performance
        pygame.display.update()
        frames_per_second = 45
        clock.tick(frames_per_second)


def game_paused():
    pass


def game_end():
    pass


def game_leaderboards():
    pass


game_menu()
