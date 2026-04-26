import unittest

from src.utils import extract_title


class TestUtils(unittest.TestCase):
    def test_extract_title(self):
        cases = [
            ("# Hello", "Hello"),
            ("some other\n stuff there\n is not a title\n # the title", "the title"),
            ("the title\n is in\n # the title \n the \n middle\n ", "the title"),
        ]
        for markdown, expected_title in cases:
            extracted_title = extract_title(markdown)
            self.assertEqual(extracted_title, expected_title)
