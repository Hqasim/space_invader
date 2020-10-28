import pygame
import os
import sys
pygame.font.init()

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (450, 50)  # Game window position

# Game Variables
game_state = 1
score = 0
lives = 3

# Game Constants
DISPLAY_WIDTH, DISPLAY_HEIGHT = 600, 750
FRAMES_PER_SECOND = 75
MAIN_FONT = pygame.font.SysFont("comicsans", 40)
PLAYER_SHIP_VELOCITY = 5


# Color definition
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Screen Setup
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Load Enemies Ship Images
BLACK_ENEMY = pygame.image.load('../Assets/enemyBlack1.png')
BLUE_ENEMY = pygame.image.load('../Assets/enemyBlue2.png')
GREEN_ENEMY = pygame.image.load('../Assets/enemyGreen4.png')
RED_ENEMY = pygame.image.load('../Assets/enemyRed5.png')

# Load Player Ship Image
PLAYER_SHIP = pygame.image.load('../Assets/playerShip1_red.png')

# Load Laser Images
BLUE_LASER = pygame.image.load('../Assets/pixel_laser_blue.png')  # Player laser color
RED_LASER = pygame.image.load('../Assets/pixel_laser_red.png')  # Enemies laser color

# Load Background Image
BACKGROUND = pygame.image.load('../Assets/background_black.png')

# Game functions


def redraw_window():
    # Draws the screen with the background
    screen.blit(BACKGROUND, (0, 0))


def redraw_score_lives():
    # Draws the screen with score and lives
    score_label = MAIN_FONT.render(f"Score: {score}", 1, WHITE)
    lives_label = MAIN_FONT.render(f"Lives: {lives}", 1, WHITE)
    screen.blit(score_label, ((DISPLAY_WIDTH - score_label.get_width() - 10), 10))
    screen.blit(lives_label, (10, 10))

# Game Classes


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


class Ship:
    def __init__(self, x, y, health=100):
        self.x = int(x)
        self.y = int(y)
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.fire_cool_down = 0

    def draw(self, window):
        window.blit(PLAYER_SHIP, (self.x, self.y))

# Game menu functions


def game_menu():
    # Buttons
    play_button = Button(RED, 100, 350, 350, 100, "Play")
    leaderboards_button = Button(RED, 100, 550, 350, 100, "Leaderboards")

    while True:
        # Set background
        redraw_window()

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
    # Player Ship
    ship = Ship((DISPLAY_WIDTH/2) - 30, DISPLAY_HEIGHT - 85)

    # Game Loop
    while True:
        # Screen Performance
        clock.tick(FRAMES_PER_SECOND)

        # Set window
        redraw_window()
        redraw_score_lives()

        # Draw Player Ship
        ship.draw(screen)

        # Window Closing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Key Input Event Handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  # Left arrow key
            ship.x -= PLAYER_SHIP_VELOCITY
        if keys[pygame.K_RIGHT]:  # Right arrow key
            ship.x += PLAYER_SHIP_VELOCITY
        if keys[pygame.K_UP]:  # Up arrow key
            ship.y -= PLAYER_SHIP_VELOCITY
        if keys[pygame.K_DOWN]:  # Down arrow key
            ship.y += PLAYER_SHIP_VELOCITY

        pygame.display.update()


def game_paused():
    pass


def game_end():
    pass


def game_leaderboards():
    pass

game_menu()
