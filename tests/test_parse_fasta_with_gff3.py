# import unittest
# from unittest.mock import patch, Mock
# from functions import parse_fasta_with_gff3

# class TestParseFastaWithGFF3(unittest.TestCase):

#     @patch('requests.get')  # Replace with the actual path to the requests.get function
#     @patch('builtins.open', new_callable=mock_open)  # Replace with the actual path to the open function
#     @patch('functions.parse_attributes')  # Replace with the actual path to the parse_attributes function
#     @patch('functions.extract_fasta_with_gff3_info')  # Replace with the actual path to the extract_fasta_with_gff3_info function
#     @patch('functions.parse_fasta_result')  # Replace with the actual path to the parse_fasta_result function
#     def test_parse_fasta_with_gff3(
#             self, mock_parse_fasta_result, mock_extract_fasta_info,
#             mock_parse_attributes, mock_open, mock_requests_get
#     ):
#         # Set up mocks for requests.get, open, parse_attributes, extract_fasta_with_gff3_info, and parse_fasta_result
#         mock_requests_get.return_value.text = 'fake_gff3_content\nline2\nline3'
#         mock_open.return_value.__enter__.return_value = Mock()
#         mock_parse_attributes.return_value = {'fake_attribute': 'fake_value'}
#         mock_extract_fasta_info.return_value = 'fake_parsed_fasta_info'
#         mock_parse_fasta_result.return_value = 'fake_result'

#         # Call the function with mock data
#         result = 'fake_fasta_result'
#         path = 'fake_path'
#         dict_ids = {'fake_ids': 'fake_values'}
#         dict_taxo = {'fake_taxo': 'fake_values'}
#         ids = ['fake_ids']
#         gene_pattern = ['fake_pattern']
#         OPTIONS = None

#         result = parse_fasta_with_gff3(result, path, dict_ids, dict_taxo, ids, gene_pattern, OPTIONS)

#         # Perform assertions
#         self.assertEqual(result, 'fake_result')
#         mock_requests_get.assert_called_once_with('fake_ncbi_url', params=Mock(), timeout=60)
#         mock_open.return_value.__enter__.return_value.write.assert_called_once_with('fake_gff3_content\nline2\nline3')
#         mock_parse_attributes.assert_called_once()
#         mock_extract_fasta_info.assert_called_once()
#         mock_parse_fasta_result.assert_called_once()

# if __name__ == '__main__':
#     unittest.main()
