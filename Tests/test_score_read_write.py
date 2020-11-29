# Test game function which read and write to persistence storage
# Score test file present in Test package named: "score_test_data.json"
import unittest
import json
from Application.game import score_append, score_read


class TestScore(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        # Resetting score_test_data.json file to default started template contents
        test_data_template = {"Space Invaders Leaderboards": []}
        with open("score_test_data.json", "w") as file:
            json.dump(test_data_template, file)

    def test_score_append(self):
        # Sample data to be tested
        score_data = {"Test Name 1": 100}
        # Append to score test file
        score_append(score_data, file="score_test_data.json")
        # read from appended score test file
        read_test_data = score_read(file="score_test_data.json")
        # Assertion check
        self.assertEqual(score_data, read_test_data[0])


if __name__ == "__main__":
    unittest.main()
