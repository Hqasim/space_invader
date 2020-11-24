# Test suit for game application
import unittest
from Application import game

print("tests activated")


class TestGame(unittest.TestCase):
    def setUp(self):
        print("Setup")

    def tearDown(self):
        print("Tear down")

    def test_application_launched(self):
        print("Test Player Ship set and get methods")
        player_ship_test = game.Player(50, 50)
        player_ship_test.set_player_name("HQ_Test")
        self.assertEqual(player_ship_test.get_player_name(), "HQ_Test")




if __name__ == "__main__":
    unittest.main()
