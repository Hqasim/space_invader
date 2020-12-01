"""Laser class used by player_ship and enemy_ship classes. Used to create laser object on screen"""
import pygame


class Laser:
    """Laser class creates a laser object with the specified image, onto GUI window

    Parameters:
        x (int): X coordinate of laser object on screen
        y (int): Y coordinate of laser object on screen
        laser_img (str): file path of laser image to be blit on screen

    """
    def __init__(self, x, y, laser_img):
        self.x = x + 33
        self.y = y - 20
        self.img = laser_img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        """Draws the laser on screen

        Parameters:
            window (object): Pygame window object on which the laser is to be displayed
        """
        window.blit(self.img, (self.x, self.y))

    # Moves the laser
    def move(self, vel):
        """Moves the laser

        Parameters:
            vel (int): Move step of laser in pixels
        """
        self.y += vel

    def off_screen(self, height):
        """Determines if laser is on GUI screen

        Parameters:
            height (int): Height of GUI window.

        Returns:
            bool: True if laser is off screen. False if laser is on screen.
        """
        return not (height >= self.y >= 0)

    # Runs the collide function between laser and object. Object can be player or enemy ship
    def collision(self, obj):
        """This method simply class the collide helper function

        Parameter:
            obj (object): Object on which laser might collide

        Returns:
            collide method. Which essentially returns True if collision happened, otherwise False
        """
        return collide(obj, self)


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
