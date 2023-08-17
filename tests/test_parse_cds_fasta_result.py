import unittest
from operator import attrgetter
import filecmp
import os
import shutil

# local import
from functions import parse_fasta_cds_result
from data import efetch_dl_cds_response, fasta_data

expected_efetch_dl_cds_normal_result = attrgetter("efecth_cds_response")(
    efetch_dl_cds_response
)
expected_normal_cds_result = attrgetter("cds_expected_returned_result")(
    efetch_dl_cds_response
)
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
    def test_parse_cds_fasta_normal_result(self):
        OPTIONS = (None, [], 2, None, None, False)  # -t option

        # should return expected result
        fasta_cds_result = parse_fasta_cds_result(
            expected_efetch_dl_cds_normal_result,  ## should mock cds
            arguments["path"],
            arguments["dict_ids"],
            arguments["dict_taxo"],
            OPTIONS,
        )
        # function output
        self.assertEqual(fasta_cds_result, expected_normal_cds_result)
        # files
        ## get the subdirectory path
        self.assertTrue(
            filecmp.cmp("./tests/data/fasta_cds_expected.fasta", "./sequences.fasta")
        )

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
        if os.path.exists("./sequences.fasta"):
            os.remove("./sequences.fasta")


if __name__ == "__main__":
    unittest.main()
