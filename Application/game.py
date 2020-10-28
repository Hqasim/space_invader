import pygame
import os
import sys
import random
pygame.font.init()

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (450, 50)  # Game window position

# System Variables
game_state = 1

# Game Constants
DISPLAY_WIDTH, DISPLAY_HEIGHT = 600, 750
FRAMES_PER_SECOND = 75
MAIN_FONT = pygame.font.SysFont("comicsans", 35)
PLAYER_SHIP_VELOCITY = 5
PLAYER_MAX_Y = 30  # keeps ship off score and lives text

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
ORANGE_ENEMY = pygame.image.load('../Assets/enemyRed5.png')

# Load Player Ship Image
PLAYER_SHIP = pygame.image.load('../Assets/playerShip1_red.png')

# Load Laser Images
BLUE_LASER = pygame.image.load('../Assets/pixel_laser_blue.png')  # Player laser color
RED_LASER = pygame.image.load('../Assets/pixel_laser_red.png')  # Enemies laser color

# Load Background Image
BACKGROUND = pygame.image.load('../Assets/background_black.png')


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
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SHIP
        self.laser_img = BLUE_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)  # for accurate collision


class Enemy(Ship):
    COLOR_MAP = {
        "black": (BLACK_ENEMY, RED_LASER),
        "blue": (BLUE_ENEMY, RED_LASER),
        "green": (GREEN_ENEMY, RED_LASER),
        "orange": (ORANGE_ENEMY, RED_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)  # for accurate collision

    def move(self, vel):
        self.y += vel


# Game menu functions


def game_menu():
    # Buttons
    play_button = Button(RED, 100, 350, 350, 100, "Play")
    leaderboards_button = Button(RED, 100, 550, 350, 100, "Leaderboards")

    while True:
        # Set background
        screen.blit(BACKGROUND, (0, 0))

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
    # Game Parameters
    level = 0
    score = 0
    lives = 3
    enemies = []
    wave_length = 5
    enemies_vel = 1

    # Game Methods
    def redraw_window():
        # Draws the screen with the background
        screen.blit(BACKGROUND, (0, 0))

    def redraw_score_lives_level():
        # Draws the screen with score and lives
        score_label = MAIN_FONT.render(f"Score: {score}", 1, WHITE)
        lives_label = MAIN_FONT.render(f"Lives: {lives}", 1, WHITE)
        level_label = MAIN_FONT.render(f"Level: {level}", 1, WHITE)
        screen.blit(score_label, ((DISPLAY_WIDTH - score_label.get_width() - 10), 10))
        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (int(DISPLAY_WIDTH / 2) - 50, 10))

    # Player Ship
    player_ship = Player((DISPLAY_WIDTH/2) - 30, DISPLAY_HEIGHT - 80)



    # Game Loop
    while True:
        # Screen Performance
        clock.tick(FRAMES_PER_SECOND)

        # Set window
        redraw_window()
        redraw_score_lives_level()

        # Spawning enemies
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, DISPLAY_WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["black", "blue", "green", "orange"]))
                enemies.append(enemy)
        for enemy in enemies:  # Moving enemies down
            enemy.draw(screen)

        # Draw Player Ship
        player_ship.draw(screen)

        # Window Closing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Key Input Event Handling and collision detection
        keys = pygame.key.get_pressed()
        # Left arrow key
        if keys[pygame.K_LEFT] and player_ship.x - PLAYER_SHIP_VELOCITY > 0:
            player_ship.x -= PLAYER_SHIP_VELOCITY
        # Right arrow key
        if keys[pygame.K_RIGHT] and player_ship.x + PLAYER_SHIP_VELOCITY + player_ship.get_width() < DISPLAY_WIDTH:
            player_ship.x += PLAYER_SHIP_VELOCITY
        # Up arrow key
        if keys[pygame.K_UP] and player_ship.y - PLAYER_SHIP_VELOCITY > PLAYER_MAX_Y:
            player_ship.y -= PLAYER_SHIP_VELOCITY
        # Down arrow key
        if keys[pygame.K_DOWN] and player_ship.y + PLAYER_SHIP_VELOCITY + player_ship.get_height() < DISPLAY_HEIGHT:
            player_ship.y += PLAYER_SHIP_VELOCITY

        # Moving enemy ships
        for enemy in enemies:
            enemy.move(enemies_vel)

        pygame.display.update()


def game_paused():
    pass


def game_end():
    pass


def game_leaderboards():
    pass


game_menu()
