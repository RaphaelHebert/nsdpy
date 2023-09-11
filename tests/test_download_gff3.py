import unittest
from unittest.mock import patch
from functions import download_gff3
import requests
import filecmp
import os


NCBI_URL = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi"


class TestDownloadGFF3(unittest.TestCase):
    def test_download_gff3_write_file(self):
        with patch("functions.requests.get") as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = "fake_gff3_content"
            mocked_get.return_value.url = "mockedURL"

            # Call the function with mock data
            ids = ["fake_id"]
            path = "."

            expected_params = {
                "db": "nuccore",
                "report": "gff3",
                "id": ",".join(ids),
                "email": "raphaelhebert18@gmail.com",
                "tool": "NSDPY",
            }
            OPTIONS = ("", "", "", "", "", "")
            result = download_gff3(ids, path, OPTIONS, write_file=True)

            # Perform assertions
            self.assertTrue(result.ok)
            self.assertEqual(result.text, "fake_gff3_content")
            self.assertEqual(result.url, "mockedURL")
            mocked_get.assert_called_once_with(
                NCBI_URL, params=expected_params, timeout=60
            )

        self.assertTrue(
            filecmp.cmp("./tests/data/test_download_expected.gff3", "./results.gff3")
        )

        if os.path.exists("./results.gff3"):
            os.remove("./results.gff3")

    def test_download_gff3_no_write_file(self):
        with patch("functions.requests.get") as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = "fake_gff3_content"
            mocked_get.return_value.url = "mockedURL"

            # Call the function with mock data
            ids = ["fake_id"]
            path = "."

            expected_params = {
                "db": "nuccore",
                "report": "gff3",
                "id": ",".join(ids),
                "email": "raphaelhebert18@gmail.com",
                "tool": "NSDPY",
            }
            OPTIONS = ("", "", "", "", "", "")
            result = download_gff3(ids, path, OPTIONS, write_file=False)

            # Perform assertions
            self.assertTrue(result.ok)
            self.assertEqual(result.text, "fake_gff3_content")
            self.assertEqual(result.url, "mockedURL")
            mocked_get.assert_called_once_with(
                NCBI_URL, params=expected_params, timeout=60
            )

        self.assertFalse(os.path.exists("./results.gff3"))

    # cleanup even if tests fail
    def test_taxids_cleanup(self):
        if os.path.exists("./results.gff3"):
            os.remove("./results.gff3")


if __name__ == "__main__":
    unittest.main()
