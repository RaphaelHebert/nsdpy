import unittest
from unittest.mock import patch

# local import
from functions import esearchquery
from constants import ESEARCH_URL


class testsFunctions(unittest.TestCase):
    @patch("functions.download")
    def test_esearchquery(self, get_content_mock):
        query = "Parnassius[Organism] AND COI[Title]"
        api_key = "somerandomkey"
        # test errors
        get_content_mock.return_value = 1
        result = esearchquery((query, api_key))
        self.assertEqual(result, {"error": "wrong address for esearch"})

        # test success
        class Response:
            json = lambda _: "hello world"

        parameters = {}
        parameters["api_key"] = api_key
        parameters["db"] = "nucleotide"
        parameters["idtype"] = "acc"
        parameters["retmode"] = "json"
        parameters["retmax"] = "0"
        parameters["usehistory"] = "y"
        parameters["term"] = query

        get_content_mock.reset_mock()
        get_content_mock.return_value = Response()

        result = esearchquery((query, api_key))
        get_content_mock.assert_called_with(parameters, ESEARCH_URL)
        self.assertEqual(result, "hello world")


if __name__ == "__main__":
    unittest.main()
