# import from standard library
import unittest
from unittest.mock import patch
import sys


# add parent directory to imports list
sys.path.insert(0, "..")

# local import
from functions import countDown, dispatch, download


class testsFunctions(unittest.TestCase):
    def test_countDown(self):
        self.assertEqual(countDown(1, 1), "100%")
        self.assertEqual(countDown(1, 0), "no job to be done")
        with self.assertRaises(ValueError):
            countDown(-1, 1)
        with self.assertRaises(ValueError):
            countDown(1, -1)

    def test_dispatch(self):

        metazoa = [
            "Eukaryota",
            "Metazoa",
            "Chordata",
            "Craniata",
            "Vertebrata",
            "Euteleostomi",
            "Mammalia",
            "Eutheria",
            "Euarchontoglires",
            "Primates",
            "Haplorrhini",
            "Catarrhini",
            "Hominidae",
            "Homo.",
        ]
        fungi = [
            "Eukaryota",
            "Fungi",
            "Dikarya",
            "Ascomycota",
            "Saccharomycotina",
            "Saccharomycetes",
            "Saccharomycetales",
            "Dipodascaceae",
            "Saprochaete.",
        ]
        plantae = [
            "Eukaryota",
            "Viridiplantae",
            "Chlorophyta",
            "core",
            "chlorophytes",
            "Trebouxiophyceae",
            "Chlorellales",
            "Chlorellaceae",
            "Chlorella clade",
            "Micractinium.",
        ]
        wrongLineage = ["monkey", "tree", "mushroom", "Yersinia pestis"]
        customTaxonomie = [
            "Primates",
            "Haplorrhini",
            "Catarrhini",
            "Hominidae",
            "Homo.",
        ]

        ##kingdoms
        self.assertEqual(dispatch(metazoa, 1), "METAZOA")
        self.assertEqual(dispatch(plantae, 1), "PLANTAE")
        self.assertEqual(dispatch(fungi, 1), "FUNGI")
        self.assertEqual(dispatch(wrongLineage, 1), "OTHERS")
        ##no option selected
        self.assertEqual(dispatch(metazoa, 2), "sequences")
        self.assertEqual(dispatch(fungi, 2), "sequences")
        ##phylums
        self.assertEqual(dispatch(wrongLineage, 0), "OTHERS")
        self.assertEqual(dispatch(plantae, 0), "Chlorophyta")
        self.assertEqual(dispatch(fungi, 0), "Ascomycota")
        self.assertEqual(dispatch(metazoa, 0), "Chordata")
        ##list of taxonomic levels
        self.assertEqual(dispatch(metazoa, customTaxonomie), "Primates")
        self.assertEqual(dispatch(metazoa, wrongLineage), "OTHERS")
        ## n rank higher than specie
        self.assertEqual(dispatch(metazoa, 3), "Homo.")
        self.assertEqual(dispatch(plantae, 5), "Chlorellaceae")
        self.assertEqual(dispatch(plantae, 50), "OTHERS")

    def test_download(self):
        ##parameters address
        parameters = {
            "db": "nucleotide",
            "idtype": "acc",
            "retmode": "json",
            "retmax": "0",
            "usehistory": "y",
            "term": "COI[Title] homo sapiens[ORGN])",
        }

        address = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

        full_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nucleotide&idtype=acc&retmode=json&retmax=0&usehistory=y&term=COI%5BTitle%5D+homo+sapiens%5BORGN%5D%29"

        with patch("functions.requests.get") as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = "Success"
            mocked_get.return_value.url = full_url

            dl_response = download(parameters, address)
            mocked_get.assert_called_with(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
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
            self.assertEqual(dl_response.url, full_url)
            self.assertEqual(dl_response.text, "Success")


if __name__ == "__main__":
    unittest.main()
