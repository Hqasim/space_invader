import pygame
import os
import sys
import random
import json
from Application import button

# Initialize font of pygame for later use
pygame.font.init()

# Initialize pygame
pygame.init()

# Set game window initial launch position
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (450, 50)

# System Global Variables
game_state = 0

# System Global Constants
DISPLAY_WIDTH, DISPLAY_HEIGHT = 600, 750
FRAMES_PER_SECOND = 75
MAIN_FONT = pygame.font.SysFont("comicsans", 35)
MENU_FONT = pygame.font.SysFont("comicsans", 60)
PLAYER_SHIP_VELOCITY = 5  # Ship move speed in pixel per frame
PLAYER_MAX_Y = 30  # Constant denotes how high the ship can travel on screen. Avoids collision with top labels

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
class Ship:
    # Abstract class. Defines general characteristics of ship

    COOL_DOWN = 30  # Fire interval

    # Default constructor. Health set to 100, can be changed while constructing
    def __init__(self, x, y, health=100):
        self.x = int(x)
        self.y = int(y)
        self.health = health
        self.ship_img = None
        self .laser_img = None
        self.lasers = []
        self.fire_cool_down = 0

    # Increments the fire_cool_down value until COOL_DOWN value and then resets it to zero.
    def cool_down(self):
        if self.fire_cool_down >= self.COOL_DOWN:
            self.fire_cool_down = 0
        elif self.fire_cool_down > 0:
            self.fire_cool_down += 1

    # Shoots the laser only when the fire_cool_down is zero.
    def shoot(self):
        if self.fire_cool_down == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.fire_cool_down = 1

    # Draws ships and lasers
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(screen)

    # Laser mechanics
    def move_lasers(self, vel, objects):
        self.cool_down()
        for laser in self.lasers:
            # Move laser. + vel moves down and -vel moves up
            laser.move(vel)
            # Remove laser if it is off screen
            if laser.off_screen(DISPLAY_HEIGHT):
                self.lasers.remove(laser)
            # Remove laser if it collides with an object and decrement its health
            elif laser.collision(objects):
                objects.health -= 10
                self.lasers.remove(laser)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    # This class is a subclass of ship class and inherits from it.
    # Defines characteristics unique to player ship

    # default constructor, with health, score and player_name as optional parameters
    def __init__(self, x, y, health=100, score=0, player_name=""):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SHIP
        self.laser_img = BLUE_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)  # for accurate collision
        self.max_health = health
        self.score = score
        self.PLAYER_NAME = player_name

    # Overriding parent class move_laser methods
    def move_lasers(self, vel, objects):
        self.cool_down()
        for laser in self.lasers:
            # Move laser. + vel moves down and -vel moves up
            laser.move(vel)
            # Remove laser if it is off screen
            if laser.off_screen(DISPLAY_HEIGHT):
                self.lasers.remove(laser)
            else:  # Remove laser if hit enemy. Increment score by 10
                for obj in objects:
                    if laser.collision(obj):
                        objects.remove(obj)
                        self.lasers.remove(laser)
                        self.score += 10

    def get_score(self):
        return self.score

    def get_health(self):
        return self.health

    def get_player_name(self):
        return self.PLAYER_NAME

    def set_health_decrement(self, num):
        self.health -= num

    def set_player_name(self, player_name):
        self.PLAYER_NAME = player_name


class Enemy(Ship):
    # This class is a subclass of ship class and inherits from it.
    # Defines characteristics unique to enemy ship

    # Defines ship color and it's laser combination. For simplicity all enemies are shooting RED_LASER
    COLOR_MAP = {
        "black": (BLACK_ENEMY, RED_LASER),
        "blue": (BLUE_ENEMY, RED_LASER),
        "green": (GREEN_ENEMY, RED_LASER),
        "orange": (ORANGE_ENEMY, RED_LASER),
    }

    # Default constructor
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)  # for accurate collision

    # Moves the enemies at a constant velocity downwards in the +y direction
    def move(self, vel):
        self.y += vel

    # Overrides the superclass shoot method. Enemy shoots lasers downwards at a fixed interval automatically
    def shoot(self):
        if self.fire_cool_down == 0:
            # Spawn laser at the current enemy ship location
            laser = Laser(self.x - 12, self.y + 55, self.laser_img)
            self.lasers.append(laser)
            self.fire_cool_down = 1


class Laser:
    # Laser class. Used by both enemy ship and player ship

    # Default constructor
    def __init__(self, x, y, img):
        self.x = x + 33
        self.y = y - 20
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # Draws the laser on the screen
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # Moves the laser
    def move(self, vel):
        self.y += vel

    # Computes if laser off the screen
    def off_screen(self, height):
        return not (height >= self.y >= 0)

    # Runs the collide function between laser and object. Object can be player or enemy ship
    def collision(self, obj):
        return collide(obj, self)

# Game functions


def collide(obj1, obj2):
    # Returns true if obj1 collides with obj2
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def game_menu():
    # Display main menu GUI

    global game_state
    game_state = 1  # Used in testing. 1 denotes game menu GUI is active

    # Buttons
    play_button = button.Button(RED, 150, 450, 300, 75, "Play")
    leaderboards_button = button.Button(RED, 150, 550, 300, 75, "Leaderboards")

    # Main loop
    while True:
        # Set background
        screen.blit(BACKGROUND, (0, 0))

        # Draw menu text
        menu_line_1 = MENU_FONT.render("Space Invaders", 1, WHITE)
        screen.blit(menu_line_1, (int(DISPLAY_WIDTH/2 - menu_line_1.get_width()/2), 150))
        menu_line_2 = MAIN_FONT.render("by Hamzah Qasim", 1, WHITE)
        screen.blit(menu_line_2, (int(DISPLAY_WIDTH/2 - menu_line_2.get_width()/2), 250))

        # Buttons draw
        play_button.draw(screen)
        leaderboards_button.draw(screen)

        # Process events
        for event in pygame.event.get():
            # Process window close button click
            if event.type == pygame.QUIT:
                game_state = 0  # Used in testing. Denotes game is closed.
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Play button clicked
                if play_button.mouse_over(pygame.mouse.get_pos()):
                    if event.button == 1:  # ensures left mouse click only
                        game_active()  # Plays the game
                # Leaderboards button clicked
                if leaderboards_button.mouse_over(pygame.mouse.get_pos()):
                    if event.button == 1:  # ensures left mouse click only
                        game_leaderboards()

        # screen refresh/update and performance
        pygame.display.update()
        frames_per_second = 45
        clock.tick(frames_per_second)


def game_active():
    # This methods runs the GUI window in which game is played

    global game_state
    game_state = 2

    # Game Parameters
    level = 0
    enemies = []
    wave_length = 5  # Number of enemies per wave
    enemies_vel = 1
    laser_vel = 3

    # Game Methods
    def redraw_window():
        # Draws the screen with the background
        screen.blit(BACKGROUND, (0, 0))

    def redraw_score_lives_level():
        # Draws game text on screen
        score_label = MAIN_FONT.render(f"Score: {player_ship.get_score()}", 1, WHITE)
        lives_label = MAIN_FONT.render(f"Health: {player_ship.get_health()}", 1, WHITE)
        level_label = MAIN_FONT.render(f"Level: {level}", 1, WHITE)
        screen.blit(score_label, ((DISPLAY_WIDTH - score_label.get_width() - 10), 10))
        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (int(DISPLAY_WIDTH / 2) - 50, 10))

    # Player Ship
    player_ship = Player((DISPLAY_WIDTH/2) - 30, DISPLAY_HEIGHT - 80)

    # Get player name and sets it as a ship object variable
    player_ship.set_player_name(user_name())

    # Game Loop
    while True:
        # Screen performance
        clock.tick(FRAMES_PER_SECOND)

        # Set window
        redraw_window()
        redraw_score_lives_level()

        # Lost condition
        if player_ship.get_health() <= 0:
            break

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

        # Window Closing event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = 0
                print(game_state)
                pygame.quit()
                sys.exit()

        # Ship movement and shoot event handling, with boundary and collision detection
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
        # Laser Shoot
        if keys[pygame.K_SPACE]:
            player_ship.shoot()

        # Moving enemy ships and enemy laser
        for enemy in enemies[:]:
            enemy.move(enemies_vel)
            enemy.move_lasers(laser_vel, player_ship)
            # If ship hits the bottom screen, decrement life and remove from list
            if enemy.y + enemy.get_height() > DISPLAY_HEIGHT:
                player_ship.set_health_decrement(10)
                enemies.remove(enemy)
            # Enemy and player collision
            if collide(enemy, player_ship):
                enemies.remove(enemy)
                player_ship.set_health_decrement(10)
            elif random.randrange(0, 2 * 60) == 1:  # Enemy shoot random frequency
                enemy.shoot()
        # Player ship laser movement
        player_ship.move_lasers(-laser_vel, enemies)

        redraw_score_lives_level()
        pygame.display.update()  # Updates window

    # Extracting score data from player object after game ends
    score_data = {player_ship.get_player_name(): player_ship.get_score()}
    # Runs the method to append and write score for the current game
    score_append(score_data)
    # When game ends, game_end method is run showing a new window with options
    game_end(player_ship.score)


# Method reads, appends and writes players name and score on JSON file
def score_append(data, file="score_data.json"):
    # Append score to existing data
    with open(file) as data_file:
        existing_data = json.load(data_file)
        temp_data = existing_data["Space Invaders Leaderboards"]
        temp_data.append(data)
    # Write score to file
    with open(file, "w") as data_file:
        json.dump(existing_data, data_file, indent=4)


def user_name():
    # This method creates a window which request username of the user
    # Player name entered by the user is returned when submit button is clicked on GUI window

    # Buttons
    submit_button = button.Button(RED, 150, 450, 300, 75, "Submit")

    # Constant to hold player name
    PLAYER_NAME = ""

    # Window loop
    while True:
        # Set background
        screen.blit(BACKGROUND, (0, 0))

        # Draw menu text
        menu_line_1 = MENU_FONT.render("Please enter player name", 1, WHITE)
        screen.blit(menu_line_1, (int(DISPLAY_WIDTH/2 - menu_line_1.get_width()/2), 150))

        # Buttons draw
        submit_button.draw(screen)

        # process events
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            # Window closing
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Button click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.mouse_over(pygame.mouse.get_pos()):
                    if event.button == 1:  # ensures left mouse click only
                        return PLAYER_NAME  # Returns player name
            # Processing user input text keys
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)  # Storing key entered
                if len(key) == 1:
                    # For upper case characters
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        # Appends key (UPPER CASE) to player name constant
                        PLAYER_NAME += key.upper()
                    else:
                        # Appends key (lower case) to player name constant
                        PLAYER_NAME += key
                # Delete character from player name if backspace is entered on keyboard
                if key == "backspace":
                    PLAYER_NAME = PLAYER_NAME[:len(PLAYER_NAME) - 1]
                # Enter space in player name
                if key == "space":
                    PLAYER_NAME = PLAYER_NAME + " "

        # Rendering Player Name On Screen as it is typed
        menu_line_2 = MAIN_FONT.render(PLAYER_NAME, 1, WHITE)
        screen.blit(menu_line_2, (int(DISPLAY_WIDTH / 2 - menu_line_1.get_width() / 2), 250))

        # screen refresh/update and performance
        pygame.display.update()
        frames_per_second = 45
        clock.tick(frames_per_second)


def game_paused():
    # Pauses the game
    # >>To be implemented<<

    global game_state
    game_state = 3


def game_end(score):
    # This methods shows the game end screen GUI window

    global game_state
    game_state = 5

    # Buttons
    play_button = button.Button(RED, 150, 450, 300, 75, "Play Again")
    leaderboards_button = button.Button(RED, 150, 550, 300, 75, "Leaderboards")

    # Main GUI window loop
    while True:
        # Set background
        screen.blit(BACKGROUND, (0, 0))

        # Draw menu text
        menu_line_1 = MENU_FONT.render("Game Over!", 1, WHITE)
        screen.blit(menu_line_1, (int(DISPLAY_WIDTH/2) - int(menu_line_1.get_width()/2), 150))
        menu_line_2 = MAIN_FONT.render(f"Score: {score}", 1, WHITE)
        screen.blit(menu_line_2, (int(DISPLAY_WIDTH/2) - int(menu_line_2.get_width()/2), 250))

        # Buttons draw
        play_button.draw(screen)
        leaderboards_button.draw(screen)

        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = 0
                print(game_state)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.mouse_over(pygame.mouse.get_pos()):
                    if event.button == 1:  # ensures left mouse click only
                        game_active()  # plays the game
                if leaderboards_button.mouse_over(pygame.mouse.get_pos()):
                    if event.button == 1:  # ensures left mouse click only
                        game_leaderboards()

        # screen refresh/update and performance
        pygame.display.update()
        frames_per_second = 45
        clock.tick(frames_per_second)


def game_leaderboards():
    # This methods shows the leaderboards GUI window

    global game_state
    game_state = 4

    # Reads JSON file for score data
    with open("score_data.json") as data_file:
        score_data = json.load(data_file)
        score_data = score_data["Space Invaders Leaderboards"]

    # Buttons
    back_button = button.Button(RED, 150, 550, 300, 75, "Back")

    # Main GUI window loop
    while True:
        # Set background
        screen.blit(BACKGROUND, (0, 0))

        # Draw menu text
        menu_line_1 = MENU_FONT.render("Leaderbaords", 1, WHITE)
        screen.blit(menu_line_1, (int(DISPLAY_WIDTH / 2) - int(menu_line_1.get_width() / 2), 50))

        # Draw score text
        line_height = 150  # used to place text on next line
        for score in score_data:
            for name in score:
                # Draw name on GUI window
                score_line_1 = MENU_FONT.render(name, 1, WHITE)
                screen.blit(score_line_1, (int(DISPLAY_WIDTH * 0.3) - int(score_line_1.get_width() / 2), line_height))
                # Draw score on GUI window
                score_line_2 = MENU_FONT.render(str(score[name]), 1, WHITE)
                screen.blit(score_line_2, (int(DISPLAY_WIDTH * 0.75) - int(score_line_2.get_width() / 2), line_height))
            # Increment line height to display next score line on a new line
            line_height += 50

        # Buttons draw
        back_button.draw(screen)

        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = 0
                print(game_state)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.mouse_over(pygame.mouse.get_pos()):
                    if event.button == 1:  # ensures left mouse click only
                        game_menu()  # plays the game

        # screen refresh/update and performance
        pygame.display.update()
        frames_per_second = 45
        clock.tick(frames_per_second)


# This is the entry point to the game. game_menu() function is run allowing user to navigate and play the application


game_menu()
