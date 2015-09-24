from doctest import DocTestSuite
import unittest
from itertools import count

import euler_tools
from euler_tools import CachedIter, AscendingCachedIter

dtests = DocTestSuite(euler_tools)

class CachedIterTests(unittest.TestCase):

    def test_infinite(self):
        evens = CachedIter(count(2, 2))

        self.assertEqual(evens[1], 4)
        self.assertEqual(evens[:2], [2, 4])
        self.assertEqual(evens[2:5], [6, 8, 10])
        self.assertEqual(evens[5:15:2], [12, 16, 20, 24, 28])
        
        evens_sliced = evens[5:]
        self.assertIsInstance(evens_sliced, CachedIter)
        self.assertEqual(evens_sliced[:2], [12, 14])

    def test_multiple_iter(self):
        """
        Multiple iterators on the same CachedIter don't affect each other
        """
        evens = CachedIter(count(2, 2))

        i1 = iter(evens)
        i2 = iter(evens)

        self.assertEqual(next(i1), 2)
        self.assertEqual(next(i2), 2)
        self.assertEqual(next(i1), 4)
        self.assertEqual(next(i2), 4)


class AscendingCachedIterTests(unittest.TestCase):
        
    def test_finite(self):
        finite = AscendingCachedIter(range(1, 10))

        self.assertIn(2, finite)
        self.assertNotIn(-3, finite)
        self.assertNotIn(20, finite)

    def test_infinte(self):
        evens = AscendingCachedIter(count(2, 2))

        self.assertIn(2, evens)
        self.assertNotIn(3, evens)

    def test_index(self):
        evens = AscendingCachedIter(count(2, 2))

        self.assertEqual(evens[4], 10)
        self.assertEqual(evens.index(10), 4)

        with self.assertRaises(ValueError):
            evens.index(3)

if __name__ == '__main__':
    unittest.main()
