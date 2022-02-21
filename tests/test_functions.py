#import from standard library
import unittest
import sys
from pathlib import Path
import os

#add parent directory to imports list
sys.path.insert(0, "..")

#local import
from functions import countDown
from functions import dispatch

class testsFunctions(unittest.TestCase):
    
    def test_countDown(self):
        self.assertEqual(countDown(1,1),'100%')
        self.assertEqual(countDown(1,0),'no job to be done')
        with self.assertRaises(ValueError):
            countDown(-1,1)
        with self.assertRaises(ValueError):
            countDown(1,-1)

    def test_dispatch(self):
        
        metazoa = ['Eukaryota', 'Metazoa', 'Chordata', 'Craniata', 'Vertebrata', 'Euteleostomi', 'Mammalia', 
        'Eutheria', 'Euarchontoglires', 'Primates', 'Haplorrhini', 'Catarrhini', 'Hominidae', 'Homo.']
        fungi = ['Eukaryota', 'Fungi', 'Dikarya', 'Ascomycota', 'Saccharomycotina','Saccharomycetes',
        'Saccharomycetales', 'Dipodascaceae', 'Saprochaete.']
        plantae = ['Eukaryota', 'Viridiplantae', 'Chlorophyta', 'core', 'chlorophytes', 'Trebouxiophyceae', 
        'Chlorellales', 'Chlorellaceae', 'Chlorella clade', 'Micractinium.']
        wrongLineage = ['monkey', 'tree','mushroom', 'Yersinia pestis']
        customTaxonomie = ['Primates', 'Haplorrhini', 'Catarrhini', 'Hominidae', 'Homo.']

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
        self.assertEqual(dispatch(plantae, 0), 'Chlorophyta')
        self.assertEqual(dispatch(fungi, 0),'Ascomycota')
        self.assertEqual(dispatch(metazoa,0), 'Chordata')
        ##list of taxonomic levels
        self.assertEqual(dispatch(metazoa, customTaxonomie), 'Primates')
        self.assertEqual(dispatch(metazoa, wrongLineage), 'OTHERS')
        ## n rank higher than specie
        self.assertEqual(dispatch(metazoa, 3), 'Homo.')
        self.assertEqual(dispatch(plantae, 5), 'Chlorellaceae')
        self.assertEqual(dispatch(plantae, 50), 'OTHERS')





        


if __name__=='__main__':
    unittest.main()
