"""
Enemy class, inherits from ship class. Used to create enemy ships onto the game screen
"""
# Enemy ship class
import pygame
from Application import ship
from Application import laser

# Load Enemies Ship Images
BLACK_ENEMY = pygame.image.load('../Assets/enemyBlack1.png')
BLUE_ENEMY = pygame.image.load('../Assets/enemyBlue2.png')
GREEN_ENEMY = pygame.image.load('../Assets/enemyGreen4.png')
ORANGE_ENEMY = pygame.image.load('../Assets/enemyRed5.png')

# Load Laser Images
RED_LASER = pygame.image.load('../Assets/pixel_laser_red.png')  # Enemies laser color


class Enemy(ship.Ship):
    """Class creates an enemy ship on screen. Inherits characteristic from ship class

    Parameters (constructor):
        x (int): X coordinate of enemy ship

        y (int): Y coordinate of enemy ship

        color (str): enter color name from the following list ["black", "blue", "green", or "orange"].
        Defines ship color

        health (int): Default parameter of enemy ship health, always set to 100, if not stated otherwise
    """

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
        self.x = int(x)
        self.y = int(y)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)  # for accurate collision
        self.fire_cool_down = 0

    def move(self, vel):
        """Moves the enemies at a constant velocity downwards in the +y direction

        Parameters:
            vel (int): Move step in pixels of enemy ship movement per frame of game
        """
        self.y += vel

    def shoot(self):
        """Makes enemy object shoot laser in downward +y direction. Override of ship shoot method.

        """
        if self.fire_cool_down == 0:
            # Spawn laser at the current enemy ship location
            laser_obj = laser.Laser(self.x - 12, self.y + 55, self.laser_img)
            self.lasers.append(laser_obj)
            self.fire_cool_down = 1
