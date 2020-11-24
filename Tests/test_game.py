# Test suit for game application
import unittest

print("tests activated")


class TestGame(unittest.TestCase):
    def setUp(self):
        print("Setup")

    def tearDown(self):
        print("Tear down")

    def test_application_launched(self):
        print("Application launched")


if __name__ == "__main__":
    unittest.main()
