# Laser class used by player_ship and enemy_ship class
import pygame


class Laser:
    # Default constructor
    def __init__(self, x, y, laser_img):
        self.x = x + 33
        self.y = y - 20
        self.img = laser_img
        self.mask = pygame.mask.from_surface(self.img)

    # Draws the laser on the screen
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # Moves the laser
    def move(self, vel):
        self.y += vel

    # Returns False if laser is off screen
    def off_screen(self, height):
        return not (height >= self.y >= 0)

    # Runs the collide function between laser and object. Object can be player or enemy ship
    def collision(self, obj):
        return collide(obj, self)


def collide(obj1, obj2):
    # Returns true if obj1 collides with obj2
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None
