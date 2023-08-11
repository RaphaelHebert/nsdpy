import unittest
from unittest.mock import patch
from operator import attrgetter
import filecmp
import os
import shutil

# local import
from functions import fasta
from data import fasta_data

expected_download_normal_result = attrgetter("fasta_expected_result")(fasta_data)
expected_normal_result = attrgetter("fasta_expected_returned_result")(fasta_data)
expected_normal_dict_id = attrgetter("fasta_expected_result_dict_id")(fasta_data)


class testsFunctions(unittest.TestCase):
    @patch("functions.download")
    def test_fasta(self, get_content_mock):
        # arguments
        path = "."
        dict_ids = expected_normal_dict_id
        dict_taxo = {}
        QUERY = ("mocked_query", "mocked_key")
        OPTIONS = (None, None, None, None, True, None)  # -t option
        list_of_ids = ["mocked_id_one", "mocked_id_two", "mocked_id_three"]

        # split in parts and passed to the mocked dl function

        # mock
        class Response:
            text = expected_download_normal_result

        get_content_mock.return_value = Response()

        # should return expected result
        fasta_result = fasta(path, dict_ids, dict_taxo, QUERY, list_of_ids, OPTIONS)
        # function output
        self.assertEqual(fasta_result, expected_normal_result)
        # files
        self.assertTrue(
            filecmp.cmp("./tests/data/fasta_expected.fasta", "./fasta/OTHERS.fasta")
        )
        self.assertTrue(
            filecmp.cmp("./tests/data/fasta_expected.tsv", "./tsv/OTHERS.tsv")
        )

    def test_fasta_cleanup(self):
        if os.path.exists("fasta/"):
            shutil.rmtree("fasta/")
        if os.path.exists("tsv/"):
            shutil.rmtree("tsv/")


if __name__ == "__main__":
    unittest.main()
