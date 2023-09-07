import unittest

from functions import read_fasta_sequence


class TestReadFastaSequence(unittest.TestCase):
    def test_empty_sequence(self):
        fasta_sequence = ""
        info_line, dna_sequence = read_fasta_sequence(fasta_sequence)
        self.assertEqual(info_line, None)
        self.assertEqual(dna_sequence, "")

    def test_single_line_sequence(self):
        fasta_sequence = "Header\nAGCTGATCG"
        info_line, dna_sequence = read_fasta_sequence(fasta_sequence)
        self.assertEqual(info_line, "Header")
        self.assertEqual(dna_sequence, "AGCTGATCG")

    def test_multi_line_sequence(self):
        fasta_sequence = "Header\nAGCTG\nATCG"
        info_line, dna_sequence = read_fasta_sequence(fasta_sequence)
        self.assertEqual(info_line, "Header")
        self.assertEqual(dna_sequence, "AGCTGATCG")

    def test_multiple_info_lines(self):
        fasta_sequence = "Header1\nAGCTG\nHeader2\nATCG"
        info_line, dna_sequence = read_fasta_sequence(fasta_sequence)
        self.assertEqual(info_line, "Header1")
        self.assertEqual(dna_sequence, "AGCTGHeader2ATCG")

    def test_extra_newlines(self):
        fasta_sequence = "\n\nHeader\nAGCTG\n\nATCG\n\n"
        info_line, dna_sequence = read_fasta_sequence(fasta_sequence)
        self.assertEqual(info_line, "Header")
        self.assertEqual(dna_sequence, "AGCTGATCG")


if __name__ == "__main__":
    unittest.main()
