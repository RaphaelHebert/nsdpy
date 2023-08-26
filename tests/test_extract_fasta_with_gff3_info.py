import unittest
from functions import extract_fasta_with_gff3_info


class TestExtractFastaWithGFF3Info(unittest.TestCase):
    def test_basic_case(self):
        result = ">Header\nAGCTGATCGAAAATTTTTAAA"
        gff3_extract_result = {"Header": {"pattern1": [(1, 5, "+"), (9, 12, "-")]}}
        gene_pattern = ["pattern1"]

        expected_output = ">Header\nAGCTGAAAA"

        result = extract_fasta_with_gff3_info(result, gff3_extract_result, gene_pattern)
        self.assertEqual(result, expected_output)

    def test_multiple_patterns(self):
        result = ">Header\nAGCTGATCGAAAATTTTTAAA"
        gff3_extract_result = {
            "Header": {
                "pattern1": [(1, 5, "+"), (9, 12, "-")],
                "pattern2": [(2, 6, "+"), (8, 11, "-")],
            },
        }
        gene_pattern = ["pattern1", "pattern2"]

        expected_output = ">Header\nAGCTGAAAA\n>Header\nGCTGAAAAT"

        result = extract_fasta_with_gff3_info(result, gff3_extract_result, gene_pattern)
        self.assertEqual(result, expected_output)

    def test_no_matching_pattern(self):
        result = ">Header\nAGCTGATCG"
        gff3_extract_result = {
            "Header": {"pattern2": [(2, 6, "+"), (8, 11, "-")]},
        }
        gene_pattern = ["pattern1"]

        expected_output = ""

        result = extract_fasta_with_gff3_info(result, gff3_extract_result, gene_pattern)
        self.assertEqual(result, expected_output)

    def test_no_matching_key(self):
        result = ">Header2\nAGCTGATCG"
        gff3_extract_result = {
            "Header": {"pattern1": [(2, 6, "+"), (8, 11, "-")]},
        }
        gene_pattern = ["pattern1"]

        expected_output = ""

        result = extract_fasta_with_gff3_info(result, gff3_extract_result, gene_pattern)
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
