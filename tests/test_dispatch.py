import unittest
from operator import attrgetter

# local import
from functions import dispatch
from data import data  #METAZOA, FUNGI, PLANTAE, WRONG_LINEAGE, CUSTOM_TAXONOMY
METAZOA, FUNGI, PLANTAE, WRONG_LINEAGE, CUSTOM_TAXONOMY = attrgetter("METAZOA", "FUNGI", "PLANTAE", "WRONG_LINEAGE", "CUSTOM_TAXONOMY")(data)

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
    


if __name__=='__main__':
    unittest.main()
