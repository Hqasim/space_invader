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
        self.x = int(x)
        self.y = int(y)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)  # for accurate collision
        self.fire_cool_down = 0

    # Moves the enemies at a constant velocity downwards in the +y direction
    def move(self, vel):
        self.y += vel

    # Overrides the superclass shoot method. Enemy shoots lasers downwards at a fixed interval automatically
    def shoot(self):
        if self.fire_cool_down == 0:
            # Spawn laser at the current enemy ship location
            laser_obj = laser.Laser(self.x - 12, self.y + 55, self.laser_img)
            self.lasers.append(laser_obj)
            self.fire_cool_down = 1
