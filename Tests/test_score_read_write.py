"""Test game function which read and write to persistence storage.
Score test file present in Test package named: "score_test_data.json"
"""
import unittest
import json
from pathlib import Path
from Application.game import score_append, score_read

# Resolved relative to this test file so the suite runs the same regardless of
# the working directory it is invoked from.
SCORE_TEST_FILE = Path(__file__).resolve().parent / "score_test_data.json"


class TestScore(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        """Resetting score_test_data.json file to default started template contents
        """
        test_data_template = {"Space Invaders Leaderboards": []}
        with open(SCORE_TEST_FILE, "w") as file:
            json.dump(test_data_template, file)

    def test_score_append_read(self):
        """Test if sample score is appended to sample test file and read accurately
        """
        # Sample data to be tested
        score_data = {"Test Name 1": 100}
        # Append to score test file
        score_append(score_data, file=SCORE_TEST_FILE)
        # read from appended score test file
        read_test_data = score_read(file=SCORE_TEST_FILE)
        # Assertion check
        self.assertEqual(score_data, read_test_data[0])


if __name__ == "__main__":
    unittest.main()
