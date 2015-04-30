from doctest import DocTestSuite
import unittest
from itertools import count

import euler_tools
from euler_tools import CachedIter, AscendingCachedIter, cached_iter

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

class CachedIterDecoratorTests(unittest.TestCase):

    def test_cached_iter(self):

        @cached_iter
        def i(start):
            yield start
            yield start-1

        a = i(3)
        self.assertIsInstance(a, CachedIter)
        self.assertNotIsInstance(a, AscendingCachedIter)
        self.assertEqual(list(a), [3, 2])
        self.assertEqual(a.cache, [3, 2])

    def test_ascending_cached_iter(self):

        @cached_iter(ascending=True)
        def k(start):
            yield start
            yield start+2

        b = k(3)
        self.assertIsInstance(b, AscendingCachedIter)

        self.assertIn(3, b)
        self.assertNotIn(4, b)
        self.assertIn(5, b)
        self.assertNotIn(6, b)

    def test_decorate_normal_function(self):

        @cached_iter()
        def foo():
            return 1

        with self.assertRaises(TypeError):
            foo()

if __name__ == '__main__':
    unittest.main()
