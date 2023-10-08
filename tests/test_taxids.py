import os
import unittest
from unittest.mock import patch
from operator import attrgetter
import filecmp

# local import
from constants import ESUMMARY_URL
from functions import taxids
from data import esummary_response

mocked_response_xms, expected_output = attrgetter(
    "mocked_response_xms", "expected_output"
)(esummary_response)

# TODO: tests stdout on different errors


class testsFunctions(unittest.TestCase):

    # @patch('sys.stdout', new_callable=io.StringIO)mock_stdout
    @patch("functions.download")
    def test_taxids(self, get_content_mock):
        sequence_1 = "1234567890"
        taxid_1 = "!@122"
        sequence_2 = "0987654321"
        taxid_2 = "#$344"
        expected_response = {}
        expected_response[sequence_1] = taxid_1
        expected_response[sequence_2] = taxid_2

        class Taxids_results:
            text = mocked_response_xms

        path = "."
        mocked_query_key = "mockedQueryKey!"
        mocked_webenv = {"web": "ok", "mocked": True}
        mocked_count = 3
        params = (mocked_query_key, mocked_webenv, mocked_count)
        parameters = {
            "api_key": "someRandomKey",
            "db": "taxonomy",
            "query_key": mocked_query_key,
            "WebEnv": mocked_webenv,
            "retstart": "0",
            "retmax": "3",
            "rettype": "uilist",
            "retmode": "text",
        }

        OPTIONS = ("", "", "", True, "", "")  # write output file
        QUERY = ("somerandomstring", "someRandomKey")
        get_content_mock.return_value = Taxids_results()
        result = taxids(params, path, QUERY, OPTIONS)
        get_content_mock.assert_called_with(parameters, ESUMMARY_URL)
        self.assertEqual(result, expected_output)
        self.assertTrue(filecmp.cmp("./tests/data/TaxIDs_expected.txt", "TaxIDs.txt"))

    def test_taxids_cleanup(self):
        # make sure the created file in test_taxids is cleaned up even on test fail
        if os.path.exists("./TaxIDs.txt"):
            os.remove("./TaxIDs.txt")


if __name__ == "__main__":
    unittest.main()
