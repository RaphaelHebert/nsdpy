import unittest

from functions import merge_and_sort_overlaps


class TestMergeAndSortOverlaps(unittest.TestCase):
    def test_empty_sequences(self):
        result = merge_and_sort_overlaps([], 10)
        self.assertEqual(result, [])

    def test_no_overlaps(self):
        sequences = [(1, 3, "+"), (5, 7, "+"), (9, 11, "+")]
        result = merge_and_sort_overlaps(sequences, 15)
        expected = [(1, 3), (5, 7), (9, 11)]
        self.assertEqual(result, expected)

    def test_with_reverse_sequences(self):
        sequences = [(1, 3, "+"), (5, 7, "-"), (9, 11, "+")]
        result = merge_and_sort_overlaps(sequences, 15)
        expected = [(1, 3), (9, 11)]
        self.assertEqual(result, expected)

    def test_with_overlaps(self):
        sequences = [(1, 5, "+"), (4, 8, "+"), (6, 10, "+")]
        result = merge_and_sort_overlaps(sequences, 15)
        expected = [(1, 10)]
        self.assertEqual(result, expected)

    def test_complex_case(self):
        sequences = [
            (1, 5, "+"),
            (3, 8, "+"),
            (7, 10, "+"),
            (12, 15, "-"),
            (12, 15, "+"),
        ]
        result = merge_and_sort_overlaps(sequences, 15)
        expected = [(1, 10), (12, 15)]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
