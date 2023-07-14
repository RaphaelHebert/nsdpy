import sys
import unittest
from unittest.mock import patch, DEFAULT

# local import
from functions import countDown

class testsFunctions(unittest.TestCase):
    
    def test_countDown(self):
        self.assertEqual(countDown(1,1),'100%')
        self.assertEqual(countDown(1,0),'no job to be done')
        with self.assertRaises(ValueError):
            countDown(-1,1)
        with self.assertRaises(ValueError):
            countDown(1,-1)


if __name__=='__main__':
    unittest.main()
