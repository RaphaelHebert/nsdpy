import unittest
from functions import insert_newline


class TestInsertNewline(unittest.TestCase):
    def test_empty_text(self):
        text = ""
        length = 10
        result = insert_newline(text, length)
        self.assertEqual(result, "")

    def test_short_text(self):
        text = "Hello"
        length = 10
        result = insert_newline(text, length)
        self.assertEqual(result, "Hello")

    def test_exact_length(self):
        text = "ABCDEFGHIJ"
        length = 10
        result = insert_newline(text, length)
        self.assertEqual(result, "ABCDEFGHIJ")

    def test_long_text(self):
        text = "ABCDEFGHIJKLM"
        length = 5
        result = insert_newline(text, length)
        expected = "ABCDE\nFGHIJ\nKLM"
        self.assertEqual(result, expected)

    def test_multiple_newlines(self):
        text = "AABBCCDDEE"
        length = 2
        result = insert_newline(text, length)
        expected = "AA\nBB\nCC\nDD\nEE"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
