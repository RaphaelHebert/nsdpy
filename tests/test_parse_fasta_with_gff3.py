import unittest
from unittest.mock import patch, Mock
from functions import parse_fasta_with_gff3
from operator import attrgetter
from data import mock_download_gff3

mock_download_gff3_result = attrgetter("mock_download_gff3_result")(mock_download_gff3)


class TestParseFastaWithGFF3(unittest.TestCase):
    @patch(
        "functions.parse_fasta_result"
    )  # Replace with the actual path to parse_fasta_result function
    @patch(
        "functions.extract_fasta_with_gff3_info"
    )  # Replace with the actual path to extract_fasta_with_gff3_info function
    @patch(
        "functions.parse_attributes"
    )  # Replace with the actual path to parse_attributes function
    @patch(
        "functions.download_gff3"
    )  # Replace with the actual path to download_gff3 function
    def test_parse_fasta_with_gff3(
        self,
        mock_download_gff3,
        mock_parse_attributes,
        mock_extract_fasta_info,
        mock_parse_fasta_result,
    ):
        # Set up mocks for download_gff3, parse_attributes, extract_fasta_with_gff3_info, and parse_fasta_result
        mock_gff3_result = Mock()
        mock_gff3_result.ok = True
        mock_gff3_result.text = mock_download_gff3_result
        mock_gff3_result.url = "fake_ncbi_url"
        mock_download_gff3.return_value = mock_gff3_result

        mock_parse_attributes.return_value = {"gene": "fake_gene", "ID": "fake_ID"}

        mock_extract_fasta_info.return_value = "fake_parsed_fasta_info"
        mock_parse_fasta_result.return_value = "fake_result"

        # Call the function with mock data
        result = "fake_fasta_result"
        path = "fake_path"
        dict_ids = {"fake_ids": "fake_values"}
        dict_taxo = {"fake_taxo": "fake_values"}
        ids = ["fake_ids"]
        gene_pattern = ["fake_pattern"]
        OPTIONS = None

        result = parse_fasta_with_gff3(
            result, path, dict_ids, dict_taxo, ids, gene_pattern, OPTIONS
        )

        # Perform assertions
        self.assertEqual(result, "fake_result")
        mock_download_gff3.assert_called_once_with(["fake_ids"], path, False)
        mock_extract_fasta_info.assert_called_once()
        self.assertEqual(mock_parse_attributes.call_count, 209)
        mock_parse_fasta_result.assert_called_once()


if __name__ == "__main__":
    unittest.main()
