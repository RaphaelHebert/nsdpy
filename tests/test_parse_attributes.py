import unittest

from functions import parse_attributes


class TestParseAttributes(unittest.TestCase):
    def test_empty_attributes(self):
        attributes_str = ""
        result = parse_attributes(attributes_str)
        self.assertEqual(result, {})

    def test_single_attribute(self):
        attributes_str = "ID=12345"
        result = parse_attributes(attributes_str)
        self.assertEqual(result, {"ID": "12345"})

    def test_multiple_attributes(self):
        attributes_str = "ID=12345;Name=Gene1;Type=Coding"
        result = parse_attributes(attributes_str)
        self.assertEqual(result, {"ID": "12345", "Name": "Gene1", "Type": "Coding"})

    def test_attributes_with_spaces(self):
        attributes_str = "ID=12345; Note=This is a note; Name=Gene1"
        result = parse_attributes(attributes_str)
        self.assertEqual(
            result, {"ID": "12345", "Note": "This is a note", "Name": "Gene1"}
        )

    def test_missing_values(self):
        attributes_str = "ID=12345;Note=;Name=Gene1"
        result = parse_attributes(attributes_str)
        self.assertEqual(result, {"ID": "12345", "Name": "Gene1"})


if __name__ == "__main__":
    unittest.main()
