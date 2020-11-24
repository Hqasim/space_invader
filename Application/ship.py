# Ship class
from Application import laser


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
            laser_obj = laser.Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser_obj)
            self.fire_cool_down = 1

    # Draws ships and lasers
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser_item in self.lasers:
            laser_item.draw(window)

    # Laser mechanics
    def move_lasers(self, vel, objects):
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
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
