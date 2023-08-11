import unittest
from unittest.mock import patch
from operator import attrgetter
import filecmp
import os
import io
import shutil

# local import
from functions import fasta
from data import fasta_data

expected_download_normal_result = attrgetter("fasta_expected_result")(fasta_data)
expected_normal_result = attrgetter("fasta_expected_returned_result")(fasta_data)
expected_normal_dict_id = attrgetter("fasta_expected_result_dict_id")(fasta_data)


def cleanup(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        if os.path.exists("tsv/"):
            shutil.rmtree("tsv/")


# mock
class Response:
    text = expected_download_normal_result


class testsFunctions(unittest.TestCase):
    @patch("functions.download")
    def test_fasta(self, get_content_mock):
        arguments = {
            "path": ".",
            "dict_ids": expected_normal_dict_id,
            "dict_taxo": {},
            "QUERY": ("mocked_query", "mocked_key"),
            "OPTIONS": (None, None, None, None, True, None),  # -t option
            "list_of_ids": ["mocked_id_one", "mocked_id_two", "mocked_id_three"],
        }

        get_content_mock.return_value = Response()

        # should return expected result
        fasta_result = fasta(
            arguments["path"],
            arguments["dict_ids"],
            arguments["dict_taxo"],
            arguments["QUERY"],
            arguments["list_of_ids"],
            arguments["OPTIONS"],
        )
        # function output
        self.assertEqual(fasta_result, expected_normal_result)
        # files
        self.assertTrue(
            filecmp.cmp("./tests/data/fasta_expected.fasta", "./fasta/OTHERS.fasta")
        )
        self.assertTrue(
            filecmp.cmp("./tests/data/fasta_expected.tsv", "./tsv/OTHERS.tsv")
        )
        cleanup("tsv/")
        cleanup("fasta/")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_fasta_stdout(self, mock_stdout):

        arguments = {
            "path": ".",
            "dict_ids": expected_normal_dict_id,
            "dict_taxo": {},
            "QUERY": ("mocked_query", "mocked_key"),
            "OPTIONS": (1, None, None, None, True, None),  # -t option
            "list_of_ids": ["mocked_id_one", "mocked_id_two", "mocked_id_three"],
        }

        with patch("functions.download") as mocked_get:
            mocked_get.side_effect = [Response()]
            fasta(
                arguments["path"],
                arguments["dict_ids"],
                arguments["dict_taxo"],
                arguments["QUERY"],
                arguments["list_of_ids"],
                arguments["OPTIONS"],
            )
            self.assertEqual(mock_stdout.getvalue(), "Downloading the fasta files...\n")

        # self.assertEqual(mock_stdout.getvalue(), "Downloading the fasta files...")
        # clear mock_stdout value
        mock_stdout.seek(0)
        mock_stdout.truncate(0)


if __name__ == "__main__":
    unittest.main()
