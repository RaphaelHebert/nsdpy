import unittest
from operator import attrgetter

# local import
from functions import parseClassifXML
from data import parseClassifXML_response_1, fetch_taxonomy_result_1
 
input_data_1 = attrgetter("response_1")(fetch_taxonomy_result_1)
result = attrgetter("result")(parseClassifXML_response_1)


class testsFunctions(unittest.TestCase):

    def test_parseClassifXML(self):
        parse_result = parseClassifXML(input_data_1)
        self.assertEqual(parse_result, result )

if __name__=='__main__':
    unittest.main()
