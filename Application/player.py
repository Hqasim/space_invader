"""
Player class, inherits from ship class. Used to create player ship onto the game screen
"""
from Application import ship
import pygame

# Load Player Ship Image
PLAYER_SHIP = pygame.image.load('../Assets/playerShip1_red.png')

# Load Laser Images
BLUE_LASER = pygame.image.load('../Assets/pixel_laser_blue.png')  # Player laser color


class Player(ship.Ship):
    """Class creates a player ship on screen. Inherits characteristic from ship class.

    Parameters (constructor):
        x (int): X coordinate of player ship

        y (int): Y coordinate of player ship

        health (int): Default parameter of enemy ship health, always set to 100, if not stated otherwise

        score (int): Player score with default value of 0

        player_name (str): Player name with a default empty string value
    """
    def __init__(self, x, y, health=100, score=0, player_name=""):
        super().__init__(x, y, health)
        self.x = int(x)
        self.y = int(y)
        self.ship_img = PLAYER_SHIP
        self.laser_img = BLUE_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)  # for accurate collision
        self.max_health = health
        self.score = score
        self.PLAYER_NAME = player_name

    # Overriding parent class move_laser methods
    def move_lasers(self, vel, objects):
        """Method overrides ship class method. Moves player ship lasers in upward -y direction

        Parameters:
             vel (int): Laser move step velocity
             objects (object list): Ideally enemy object list would be passed here
        """

        self.cool_down()
        for laser in self.lasers:
            # Move laser. + vel moves down and -vel moves up
            laser.move(vel)
            # Remove laser if it is off screen
            if laser.off_screen(750):  # 750 is display height
                self.lasers.remove(laser)
            else:  # Remove laser if hit enemy. Increment score by 10
                for obj in objects:
                    if laser.collision(obj):
                        objects.remove(obj)
                        self.lasers.remove(laser)
                        self.score += 10

    def get_score(self):
        """Methods returns player score

        Returns:
            int: Player score
        """
        return self.score

    def get_health(self):
        """Methods returns player health

        Returns:
            int: Player health
        """
        return self.health

    def get_player_name(self):
        """Methods returns player name

        Returns:
            str: Player name
        """
        return self.PLAYER_NAME

    def set_health_decrement(self, num):
        """Methods decrements player health

        Parameters:
            num (int): Number to decrement player health with

        """
        self.health -= num

    def set_player_name(self, player_name):
        """Methods sets player name

        Parameters:
            player_name (str): Player name as string to be set as object property

        """
        self.PLAYER_NAME = player_name
