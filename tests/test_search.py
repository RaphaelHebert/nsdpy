import unittest
from operator import attrgetter

# local import
from functions import search
from data import search_data
 
dna_1, seq_1, response_1 = attrgetter("dna_1", "seq_1", "response_1")(search_data)


class testsFunctions(unittest.TestCase):

    def test_search(self):
        # should parse data correctly
        parse_result = search(dna_1 ,{}, seq_1)
        self.assertDictEqual(parse_result, response_1)
        
if __name__=='__main__':
    unittest.main()
