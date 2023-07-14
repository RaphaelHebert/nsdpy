import sys
import io
import os
import unittest
from unittest.mock import patch, DEFAULT
import requests
import filecmp
from operator import attrgetter

# add parent directory to imports list
sys.path.insert(0, "..")

# add data
sys. path.insert(0,'./data') 

# add data
sys. path.insert(0,'./xmls') 

# local import

from constants import EFETCH_URL, ESUMMARY_URL, ESEARCH_URL
from functions import countDown, dispatch, download, esearchquery, taxids
from data import data, esummary_response  #METAZOA, FUNGI, PLANTAE, WRONG_LINEAGE, CUSTOM_TAXONOMY
METAZOA, FUNGI, PLANTAE, WRONG_LINEAGE, CUSTOM_TAXONOMY = attrgetter("METAZOA", "FUNGI", "PLANTAE", "WRONG_LINEAGE", "CUSTOM_TAXONOMY")(data)
mocked_response_xms , expected_output = attrgetter("mocked_response_xms", "expected_output")(esummary_response)

class testsFunctions(unittest.TestCase):

    def test_dispatch(self):
    
        ##kingdoms
        self.assertEqual(dispatch(METAZOA, 1), "METAZOA")
        self.assertEqual(dispatch(PLANTAE, 1), "PLANTAE")
        self.assertEqual(dispatch(FUNGI, 1), "FUNGI")
        self.assertEqual(dispatch(WRONG_LINEAGE, 1), "OTHERS")
        ##no option selected
        self.assertEqual(dispatch(METAZOA, 2), "sequences")
        self.assertEqual(dispatch(FUNGI, 2), "sequences")
        ##phylums
        self.assertEqual(dispatch(WRONG_LINEAGE, 0), "OTHERS")
        self.assertEqual(dispatch(PLANTAE, 0), 'Chlorophyta')
        self.assertEqual(dispatch(FUNGI, 0),'Ascomycota')
        self.assertEqual(dispatch(METAZOA,0), 'Chordata')
        ##list of taxonomic levels
        self.assertEqual(dispatch(METAZOA, CUSTOM_TAXONOMY), 'Primates')
        self.assertEqual(dispatch(METAZOA, WRONG_LINEAGE), 'OTHERS')
        ## n rank higher than specie
        self.assertEqual(dispatch(METAZOA, 3), 'Homo.')
        self.assertEqual(dispatch(PLANTAE, 5), 'Chlorellaceae')
        self.assertEqual(dispatch(PLANTAE, 50), 'OTHERS')
    

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_download(self, mock_stdout): 
        ##parameters address
        parameters = {
            'db': 'nucleotide', 
            'idtype': 'acc', 
            'retmode': 'json', 
            'retmax': '0', 
            'usehistory': 'y', 
            'term': 'COI[Title] homo sapiens[ORGN])'}


        HTTP_ERROR = requests.exceptions.HTTPError('404, bad url')
        TIMEOUT_ERROR = requests.exceptions.Timeout('connection timed out')
        CONNECTION_ERROR = requests.exceptions.ConnectionError
        REQUEST_EXCEPTION_ERROR = requests.exceptions.RequestException('exception error')

        HTTP_ERROR_RESPONSE = "Http Error: " + HTTP_ERROR.__str__() + "\n"
        TIMEOUT_ERROR_RESPONSE = f'Connection Timed out\n{TIMEOUT_ERROR}\n'
        CONNECTION_ERROR_RESPONSE = f'Connection error (please reconnect)\n \n'
        REQUEST_EXCEPTION_ERROR_RESPONSE = f'An exception occurred:\n{REQUEST_EXCEPTION_ERROR}\n'


        expected_url = f'{ESEARCH_URL}?db=nucleotide&idtype=acc&retmode=json&retmax=0&usehistory=y&term=COI%5BTitle%5D+homo+sapiens%5BORGN%5D%29'

        # url should be proceed correctly
        with patch("functions.requests.get") as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = "Success"
            mocked_get.return_value.url = expected_url

            dl_response = download(parameters, ESEARCH_URL)
            mocked_get.assert_called_with(ESEARCH_URL , params={'db': 'nucleotide', 'idtype': 'acc', 'retmode': 'json', 'retmax': '0', 'usehistory': 'y', 'term': 'COI[Title] homo sapiens[ORGN])'}, timeout=60)
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
    

    @patch('functions.download')
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


    # @patch('sys.stdout', new_callable=io.StringIO)mock_stdout
    @patch('functions.download')
    def test_taxids(self, get_content_mock ):
        sequence_1 = '1234567890'
        taxid_1 = '!@122'
        sequence_2 = '0987654321'
        taxid_2 = '#$344'
        expected_response = {}
        expected_response[sequence_1]=taxid_1
        expected_response[sequence_2]=taxid_2

        class Taxids_results:
            text = mocked_response_xms

        path = '.'
        mocked_query_key = "mockedQueryKey!"
        mocked_webenv = { "web": 'ok', 'mocked': True }
        mocked_count = 600 
        params = (mocked_query_key, mocked_webenv, mocked_count)
        parameters = {}
        parameters['db'] = "taxonomy"
        parameters['query_key'] = mocked_query_key
        parameters['WebEnv'] = mocked_webenv
        parameters['retstart'] = '400' # take the latest call, here with mocked_count = 600
        parameters['retmax'] = '200'
        parameters['rettype'] = "uilist"
        parameters['retmode'] = "text"

        OPTIONS = ("","","",True,"","") #write output file 

        get_content_mock.return_value = Taxids_results()
        result = taxids(params, path, OPTIONS)
        self.assertEqual(get_content_mock.call_count, 3)
        get_content_mock.assert_called_with(parameters, ESUMMARY_URL)
        self.assertEqual(result, expected_output)
        self.assertTrue(filecmp.cmp("./tests/data/TaxIDs_expected.txt", 'TaxIDs.txt'))

    def test_taxids_cleanup(self):
        # this is to make sure the created file in test_taxids is cleaned up even on test fail
        if os.path.exists('./TaxIDs.txt'): 
            os.remove('./TaxIDs.txt')
        print(os.getcwd())
        print(os.listdir('.'))

if __name__=='__main__':
    unittest.main()
