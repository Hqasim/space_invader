"""
Game class includes the game state methods along with game helper classes. It is responsible for the game mechanics

"""
import json
import os
import random
import sys

import pygame

from Application import player, enemy, button

# Initialize font of pygame for later use
pygame.font.init()

# Initialize pygame
pygame.init()

# Set game window initial launch position
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (450, 50)

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

# Load Background Image
BACKGROUND = pygame.image.load('../Assets/background_black.png')

# Game functions


def collide(obj1, obj2):
    """Collision Detection method computes if two objects collided on screen

    Parameters:
        obj1 (object): First object for collision comparison
        obj2 (object): Second object for collision comparison

    Returns:
            bool: True if obj1 collides with obj 2
    """
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def score_append(data, file="score_data.json"):
    """Method appends player name and score on JSON persistent storage file

        Parameters:
            data (dict): data to be appended
            file (str): name of the file. if file not in same directory as game.py, use full system path instead

    """
    # Append score to existing data
    with open(file) as data_file:
        existing_data = json.load(data_file)
        temp_data = existing_data["Space Invaders Leaderboards"]
        temp_data.append(data)
    # Write score to file
    with open(file, "w") as data_file:
        json.dump(existing_data, data_file, indent=4)


def score_read(file="score_data.json"):
    """Method reads data from JSON persistent storage file

        Parameters:
            file (str): name of the file. if file not in same directory as game.py, use full system path instead

        Returns:
            data (dict): the data read from the file
    """
    with open(file) as data_file:
        data = json.load(data_file)
        data = data["Space Invaders Leaderboards"]
    return data


# Game states functions


def game_menu():
    """Game state function. Responsible for following mechanics: Play button, Leaderboards button and close window.
    Event listeners listen to events and switch game states accordingly, by calling the appropriate game state methods.

    """

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
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Play button clicked
                if play_button.mouse_over(pygame.mouse.get_pos()):
                    if event.button == 1:  # ensures left mouse click only
                        # Plays the game
                        game_active()
                # Leaderboards button clicked
                if leaderboards_button.mouse_over(pygame.mouse.get_pos()):
                    if event.button == 1:  # ensures left mouse click only
                        game_leaderboards()
        # screen refresh/update and performance
        pygame.display.update()
        frames_per_second = 45
        clock.tick(frames_per_second)


def game_active():
    """Game state function. Responsible for following mechanics: Spcae Invader game mechanics and window close.
    Player ship is controlled with arrow keys and laser is shot using space bar. Once game is over, score is displayed.

    """
    # Game Parameters
    level = 0
    enemies = []
    wave_length = 5  # Number of enemies per wave
    enemies_vel = 1
    laser_vel = 3

    # Game Methods
    def redraw_window():
        """Draws the game screen with imported background

        """
        screen.blit(BACKGROUND, (0, 0))

    def redraw_score_lives_level():
        """Draws Score, Health, and Level on screen.

        """
        score_label = MAIN_FONT.render(f"Score: {player_ship.get_score()}", 1, WHITE)
        lives_label = MAIN_FONT.render(f"Health: {player_ship.get_health()}", 1, WHITE)
        level_label = MAIN_FONT.render(f"Level: {level}", 1, WHITE)
        screen.blit(score_label, ((DISPLAY_WIDTH - score_label.get_width() - 10), 10))
        screen.blit(lives_label, (10, 10))
        screen.blit(level_label, (int(DISPLAY_WIDTH / 2) - 50, 10))

    # Player Ship
    player_ship = player.Player(int((DISPLAY_WIDTH/2) - 30), int(DISPLAY_HEIGHT - 80))

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
                enemy_obj = enemy.Enemy(random.randrange(50, DISPLAY_WIDTH - 100), random.randrange(-1500, -100),
                                        random.choice(["black", "blue", "green", "orange"]))
                enemies.append(enemy_obj)
        for enemy_obj in enemies:  # Moving enemies down
            enemy_obj.draw(screen)

        # Draw Player Ship
        player_ship.draw(screen)

        # Window Closing event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        for enemy_obj in enemies[:]:
            enemy_obj.move(enemies_vel)
            enemy_obj.move_lasers(laser_vel, player_ship)
            # If ship hits the bottom screen, decrement life and remove from list
            if enemy_obj.y + enemy_obj.get_height() > DISPLAY_HEIGHT:
                player_ship.set_health_decrement(10)
                enemies.remove(enemy_obj)
            # Enemy and player collision
            if collide(enemy_obj, player_ship):
                enemies.remove(enemy_obj)
                player_ship.set_health_decrement(10)
            elif random.randrange(0, 2 * 60) == 1:  # Enemy shoot random frequency
                enemy_obj.shoot()
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


def user_name():
    """Game state function. Responsible for following mechanics: Enter player name on screen, extract entered player
    name via submit button and window close. Submit button calls the game_active method to run the game.

    Returns:
        str: Player name entered by user on screen, is returned when submit button is clicked

    """
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


def game_end(score):
    """Game state function. Responsible for following mechanics: Play again button, Leaderboards button and close
    window. This menu also shows the game score for the preceding game run.
    Event listeners listen to events and switch game states accordingly, by calling the appropriate game state methods.

    """
    # This methods shows the game end screen GUI window

    # Buttons
    play_button = button.Button(RED, 150, 450, 300, 75, "Play Again")
    leaderboards_button = button.Button(RED, 150, 550, 300, 75, "Leaderboards")

    # Main GUI window loop
    while True:
        # Set background
        screen.blit(BACKGROUND, (0, 0))

        # Draw menu text and score
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
    """Game state function. Responsible for following mechanics: Back button and window close button. This game state
    class game helper functions to read score data from persistent storage and display them on GUI window.
    Event listeners listen to events and switch game states accordingly, by calling the appropriate game state methods.

    """
    # Reads JSON file for score data
    score_data = score_read()

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
