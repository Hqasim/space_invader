"""Unittest game classes and their methods for their functionality
"""
import unittest
from Application.ship import Ship
from Application.player import Player
from Application.enemy import Enemy
from Application.laser import Laser


class TestGameClasses(unittest.TestCase):
    def test_ship_cool_down_increment(self):
        """cool_down method of ship class increments the value to fire_cool_down variable by 1 if initial value greater
        than zero. If value reaches 30, the variable value is reset to zero Test checks if ship cool_down method
        increments fire_cool_down variable by 1.
        """
        # Create ship object at (50, 50) screen coordinate
        ship_test = Ship(50, 50)
        # Set ship fire cool down
        ship_test.fire_cool_down = 1
        # Run cool down method to increment fire_cool_down value by 1
        ship_test.cool_down()
        # Store incremented value
        incremented_cool_down = ship_test.fire_cool_down
        # Compare values.
        self.assertEqual(2, incremented_cool_down)

    def test_ship_cool_down_reset(self):
        """Test checks id ship cool_down method resets the fire_cool_down variable to 0
        """
        # Create ship object at (50, 50) screen coordinate
        ship_test = Ship(50, 50)
        # Set ship fire cool down
        ship_test.fire_cool_down = 30
        # Run cool down method to reset fire_cool_down value to 0
        ship_test.cool_down()
        # Store reset value
        reset_cool_down = ship_test.fire_cool_down
        # Compare values.
        self.assertEqual(0, reset_cool_down)

    def test_player_shoot_zero_cool_down(self):
        """shoot method of ship class checks if fire_cool_down is zero. Only then it creates a laser object and appends
        it to an initially empty lasers list.
        Test checks if shoot method with zero default fire_cool_down
        """
        # Create player object at (50, 50) screen coordinate
        player_test = Player(50, 50)
        # Run shoot method, which creates a laser object and appends it to initially empty lasers list
        player_test.shoot()
        # Check if lasers list not empty
        self.assertNotEqual(player_test.lasers, [])

    def test_player_shoot_not_zero_cool_down(self):
        """Test checks if shoot method with fire_cool_down greater than zero
        """
        # Create player object at (50, 50) screen coordinate
        player_test = Player(50, 50)
        # Changes fire_cool_down
        player_test.fire_cool_down = 10
        # Run shoot method, which creates a laser object and appends it to initially empty lasers list
        player_test.shoot()
        # Check if lasers list is empty
        self.assertEqual(player_test.lasers, [])

    def test_enemy_move(self):
        """Test checks the move method of enemy class
        """
        # Create enemy object at (50, 50) screen coordinate
        enemy_test = Enemy(50, 50, "black")
        # Move the enemy ship
        move_step = 5  # Pixels
        enemy_test.move(move_step)
        # Check if enemy has moved
        self.assertEqual(enemy_test.get_y(), 50 + move_step)

    def test_laser_move(self):
        """Test laser move in y direction
        """
        # Create player object at (50, 100), mainly to get player laser image for laser object creation
        player_test = Player(50, 100)
        # Create a laser object at (50, 50 screen coordinate)
        laser_test = Laser(50, 50, player_test.laser_img)
        # Run the move method
        initial_y = laser_test.y
        move_step = 5
        laser_test.move(move_step)
        # Check move distance
        self.assertEqual(laser_test.y, initial_y + move_step)

    def test_laser_off_screen(self):
        """Test if laser is off screen
        """
        # Create player object at (50, 100), mainly to get player laser image for laser object creation
        player_test = Player(50, 100)
        # Create a laser object at (50, 50 screen coordinate)
        laser_test = Laser(50, 50, player_test.laser_img)
        # Declare screen height
        screen_height = 750  # Pixels
        # Run off_screen method. Returns false if laser on screen
        bool_return = laser_test.off_screen(screen_height)
        # check if off screen
        self.assertEqual(False, bool_return)


if __name__ == "__main__":
    unittest.main()
