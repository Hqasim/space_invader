"""
Helper module designed to ease button creation on GUI window using pygame module
"""
import pygame


class Button:
    """Class creates a button on the screen

    Parameters (constructor):
        color ((int),(int),(int)): Color in the form of RGB value (0,0,0) to (255,255,255)

        x (int): X coordinate of button

        y (int): Y coordinate of button

        width (int): Width of the button

        height (int): Height of the button

        text (str): Text to be displayed on the button
    """
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win):
        """Draws button surface on screen

        Parameters:
            win (object): Pygame window object to draw the button on
        """
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        # Draws text
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width // 2 - text.get_width() // 2),
                self.y + (self.height // 2 - text.get_height() // 2)))

    def mouse_over(self, pos):
        """Determine if mouse if over the button

        Parameters:
            pos((int),(int)): tuple containing mouse position (x, y) coordinates

        Returns:
            bool: True if move over button area. False if mouse not over button area.
        """
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False
