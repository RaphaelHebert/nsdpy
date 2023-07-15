import sys
import io
import unittest
from unittest.mock import patch, DEFAULT
import requests
from operator import attrgetter

# add parent directory to imports list
sys.path.insert(0, "..")

# add data
sys.path.insert(0, "./data")

# add data
sys.path.insert(0, "./xmls")

# local import

from constants import ESEARCH_URL
from functions import download
from data import (
    data,
    esummary_response,
)  # METAZOA, FUNGI, PLANTAE, WRONG_LINEAGE, CUSTOM_TAXONOMY

METAZOA, FUNGI, PLANTAE, WRONG_LINEAGE, CUSTOM_TAXONOMY = attrgetter(
    "METAZOA", "FUNGI", "PLANTAE", "WRONG_LINEAGE", "CUSTOM_TAXONOMY"
)(data)
mocked_response_xms, expected_output = attrgetter(
    "mocked_response_xms", "expected_output"
)(esummary_response)


class testsFunctions(unittest.TestCase):
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_download(self, mock_stdout):
        ##parameters address
        parameters = {
            "db": "nucleotide",
            "idtype": "acc",
            "retmode": "json",
            "retmax": "0",
            "usehistory": "y",
            "term": "COI[Title] homo sapiens[ORGN])",
        }

        HTTP_ERROR = requests.exceptions.HTTPError("404, bad url")
        TIMEOUT_ERROR = requests.exceptions.Timeout("connection timed out")
        CONNECTION_ERROR = requests.exceptions.ConnectionError
        REQUEST_EXCEPTION_ERROR = requests.exceptions.RequestException(
            "exception error"
        )

        HTTP_ERROR_RESPONSE = "Http Error: " + HTTP_ERROR.__str__() + "\n"
        TIMEOUT_ERROR_RESPONSE = f"Connection Timed out\n{TIMEOUT_ERROR}\n"
        CONNECTION_ERROR_RESPONSE = f"Connection error (please reconnect)\n \n"
        REQUEST_EXCEPTION_ERROR_RESPONSE = (
            f"An exception occurred:\n{REQUEST_EXCEPTION_ERROR}\n"
        )

        expected_url = f"{ESEARCH_URL}?db=nucleotide&idtype=acc&retmode=json&retmax=0&usehistory=y&term=COI%5BTitle%5D+homo+sapiens%5BORGN%5D%29"

        # url should be proceed correctly
        with patch("functions.requests.get") as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = "Success"
            mocked_get.return_value.url = expected_url

            dl_response = download(parameters, ESEARCH_URL)
            mocked_get.assert_called_with(
                ESEARCH_URL,
                params={
                    "db": "nucleotide",
                    "idtype": "acc",
                    "retmode": "json",
                    "retmax": "0",
                    "usehistory": "y",
                    "term": "COI[Title] homo sapiens[ORGN])",
                },
                timeout=60,
            )
            self.assertEqual(dl_response.url, expected_url)
            self.assertEqual(dl_response.text, "Success")

        # HTTP ERROR error handling
        with patch("functions.requests.get") as mocked_get:
            mocked_get.side_effect = HTTP_ERROR
            dl_response = download(parameters, ESEARCH_URL)

            self.assertEqual(mock_stdout.getvalue(), HTTP_ERROR_RESPONSE)
            self.assertEqual(dl_response, 1)

        # clear mock_stdout value
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        # TIMEOUT ERROR error handling
        with patch("functions.requests.get") as mocked_get:
            mocked_get.side_effect = [TIMEOUT_ERROR, DEFAULT]
            dl_response = download(parameters, ESEARCH_URL)
            self.assertEqual(mock_stdout.getvalue(), TIMEOUT_ERROR_RESPONSE)

        # clear mock_stdout value
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        # CONNECTION ERROR error handling
        with patch("functions.requests.get") as mocked_get:
            mocked_get.side_effect = [CONNECTION_ERROR, CONNECTION_ERROR, DEFAULT]
            dl_response = download(parameters, ESEARCH_URL)
            self.assertEqual(mock_stdout.getvalue(), CONNECTION_ERROR_RESPONSE)

        # clear mock_stdout value
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        # EXCEPTIONS ERROR error handling
        with patch("functions.requests.get") as mocked_get:
            mocked_get.side_effect = [REQUEST_EXCEPTION_ERROR, DEFAULT]
            dl_response = download(parameters, ESEARCH_URL)
            self.assertEqual(mock_stdout.getvalue(), REQUEST_EXCEPTION_ERROR_RESPONSE)


if __name__ == "__main__":
    unittest.main()
