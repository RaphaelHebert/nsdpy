import unittest
from operator import attrgetter
import filecmp
import os
import shutil

# local import
from functions import parse_fasta_result
from data import fasta_data

expected_download_normal_result = attrgetter("fasta_expected_result")(fasta_data)
expected_normal_result = attrgetter("fasta_expected_returned_result")(fasta_data)
expected_normal_dict_id = attrgetter("fasta_expected_result_dict_id")(fasta_data)


def cleanup(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        if os.path.exists("tsv/"):
            shutil.rmtree("tsv/")


arguments = {
    "path": ".",
    "dict_ids": expected_normal_dict_id,
    "dict_taxo": {},
    "QUERY": ("mocked_query", "mocked_key"),
    "list_of_ids": ["mocked_id_one", "mocked_id_two", "mocked_id_three"],
}


class testsFunctions(unittest.TestCase):
    def test_parse_fasta_result(self):
        OPTIONS = (None, None, None, None, True, None)  # -t option

        # should return expected result
        fasta_result = parse_fasta_result(
            expected_download_normal_result,
            arguments["path"],
            arguments["dict_ids"],
            arguments["dict_taxo"],
            OPTIONS,
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

    # @patch("sys.stdout", new_callable=io.StringIO)
    # def test_fasta_stdout(self, mock_stdout):
    #     OPTIONS = (2, None, None, None, True, None)  # -t option

    #     with patch("functions.download") as mocked_dl:
    #         mocked_dl.side_effect = [Response()]
    #         with patch("functions.countDown") as mocked_countDown:
    #             # mock countDown output
    #             mocked_countDown.side_effect = ["countDownResult"]
    #             parse_fasta_result(
    #                 arguments["path"],
    #                 arguments["dict_ids"],
    #                 arguments["dict_taxo"],
    #                 arguments["QUERY"],
    #                 arguments["list_of_ids"],
    #                 OPTIONS,
    #             )
    #             # get the arguments countDown is called with
    #             args = mocked_countDown.call_args.args

    #             self.assertEqual(
    #                 mock_stdout.getvalue(),
    #                 "Downloading the fasta files...\ncountDownResult\n",
    #             )
    #             self.assertEqual(args, (0, 1, "Downloading the fasta files"))

    #     # clear mock_stdout value
    #     mock_stdout.seek(0)
    #     mock_stdout.truncate(0)

    #     cleanup("tsv/")
    #     cleanup("fasta/")

    def test_taxids_cleanup(self):
        # cleanup in case a test fail
        cleanup("tsv/")
        cleanup("fasta/")


if __name__ == "__main__":
    unittest.main()
