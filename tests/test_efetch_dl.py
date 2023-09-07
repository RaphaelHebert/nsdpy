import unittest
from unittest.mock import patch
from operator import attrgetter
import os
import io
import shutil

# local import
from functions import efetch_dl
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


def mocked_callback_one(result, path, dict_ids, dict_taxo, OPTIONS):
    return ["ID1"]


arguments = {
    "path": ".",
    "dict_ids": expected_normal_dict_id,
    "dict_taxo": {},
    "QUERY": ("mocked_query", "mocked_key"),
    "list_of_ids": ["mocked_id_one", "mocked_id_two", "mocked_id_three"],
}


class testsFunctions(unittest.TestCase):
    @patch("functions.download")
    def test_efetch_dl(self, get_content_mock):
        OPTIONS = (None, None, None, None, True, None)  # -t option
        get_content_mock.return_value = Response()

        # should return expected result
        efetch_dl_result = efetch_dl(
            arguments["QUERY"],
            arguments["list_of_ids"],
            mocked_callback_one,
            arguments["path"],
            arguments["dict_ids"],
            arguments["dict_taxo"],
            "nuccore",
            "fasta",
            "text",
            OPTIONS,
        )

        # function output
        self.assertEqual(efetch_dl_result, ["ID1"])

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_efetch_dl_stdout(self, mock_stdout):
        OPTIONS = (2, None, None, None, True, None)  # -t option

        with patch("functions.download") as mocked_dl:
            mocked_dl.side_effect = [Response()]
            with patch("functions.countDown") as mocked_countDown:
                # mock countDown output
                mocked_countDown.side_effect = ["countDownResult"]
                efetch_dl(
                    arguments["QUERY"],
                    arguments["list_of_ids"],
                    mocked_callback_one,
                    arguments["path"],
                    arguments["dict_ids"],
                    arguments["dict_taxo"],
                    "nuccore",
                    "fasta",
                    "text",
                    OPTIONS,
                )
                # get the arguments countDown is called with
                args = mocked_countDown.call_args.args

                self.assertEqual(
                    mock_stdout.getvalue(),
                    "Downloading the fasta files...\ncountDownResult\n",
                )
                self.assertEqual(args, (0, 1, "Downloading the fasta files"))

        # clear mock_stdout value
        mock_stdout.seek(0)
        mock_stdout.truncate(0)


if __name__ == "__main__":
    unittest.main()
