import unittest
from unittest.mock import patch

# local import
from functions import esearchquery
from constants import ESEARCH_URL, EMAIL, TOOL


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

        parameters = {
            "email": EMAIL,
            "tool": TOOL,
            "api_key": api_key,
            "db": "nucleotide",
            "idtype": "acc",
            "retmode": "json",
            "retmax": "0",
            "usehistory": "y",
            "term": query,
        }

        get_content_mock.reset_mock()
        get_content_mock.return_value = Response()

        result = esearchquery((query, api_key))
        get_content_mock.assert_called_with(parameters, ESEARCH_URL)
        self.assertEqual(result, "hello world")


if __name__ == "__main__":
    unittest.main()
