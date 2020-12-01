"""Ship abstract class. Used to define general characteristics of player and enemy ship
"""
from Application import laser


class Ship:
    """Abstract class defines general characteristics of ship

    Parameters:
        x (int): Ship X coordinate on screen
        y (int): Ship Y coordinate on screen
        health(int): Ship health, default value is set to 100
    """
    COOL_DOWN = 30  # Fire interval

    def __init__(self, x, y, health=100):
        self.x = int(x)
        self.y = int(y)
        self.health = health
        self.ship_img = None
        self .laser_img = None
        self.lasers = []
        self.fire_cool_down = 0

    def cool_down(self):
        """Increments the fire_cool_down value until COOL_DOWN value and then resets it to zero.

        Returns:
            fire_cool_down (int): Returns the ship parameter of fire_cool_down
        """
        if self.fire_cool_down >= self.COOL_DOWN:
            self.fire_cool_down = 0
            return self.fire_cool_down
        elif self.fire_cool_down > 0:
            self.fire_cool_down += 1
            return self.fire_cool_down

    def shoot(self):
        """Shoots the laser only when the fire_cool_down is zero.
        """
        if self.fire_cool_down == 0:
            laser_obj = laser.Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser_obj)
            self.fire_cool_down = 1

    def draw(self, window):
        """Draws ships and lasers

        Parameters:
             window (object): Pygame window screen object, on which ship and lasers are to be drawn
        """
        window.blit(self.ship_img, (self.x, self.y))
        for laser_item in self.lasers:
            laser_item.draw(window)

    def move_lasers(self, vel, objects):
        """Move laser mechanics. Move laser up or down depending on velocity

        Parameters:
             vel (int): Laser move step velocity
             objects (object list): Ideally enemy object list would be passed here
        """

        self.cool_down()
        for laser_item in self.lasers:
            # Move laser. + vel moves down and -vel moves up
            laser_item.move(vel)
            # Remove laser if it is off screen
            if laser_item.off_screen(750):  # Screen height
                self.lasers.remove(laser_item)
            # Remove laser if it collides with an object and decrement its health
            elif laser_item.collision(objects):
                objects.health -= 10
                self.lasers.remove(laser_item)

    def get_width(self):
        """Gets the width of the the ship imported image

        Returns:
            float: Ship image width
        """
        return self.ship_img.get_width()

    def get_height(self):
        """Gets the height of the the ship imported image

        Returns:
            float: Ship image height
        """
        return self.ship_img.get_height()

    def get_x(self):
        """Getter for ship x property

        Returns:
            int: Ship x coordinate
        """
        return self.x

    def get_y(self):
        """Getter for ship y property

        Returns:
            int: Ship y coordinate
        """
        return self.y
