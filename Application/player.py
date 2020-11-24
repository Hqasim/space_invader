from Application import ship
import pygame

# Load Player Ship Image
PLAYER_SHIP = pygame.image.load('../Assets/playerShip1_red.png')

# Load Laser Images
BLUE_LASER = pygame.image.load('../Assets/pixel_laser_blue.png')  # Player laser color


class Player(ship.Ship):
    # This class is a subclass of ship class and inherits from it.
    # Defines characteristics unique to player ship

    # default constructor, with health, score and player_name as optional parameters
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
        return self.score

    def get_health(self):
        return self.health

    def get_player_name(self):
        return self.PLAYER_NAME

    def set_health_decrement(self, num):
        self.health -= num

    def set_player_name(self, player_name):
        self.PLAYER_NAME = player_name
