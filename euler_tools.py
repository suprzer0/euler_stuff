""" 
Various stuff I've written to help w/ solving project euler problems

python 2.6+
"""

from functools import reduce
from itertools import islice, count, chain, combinations
import math
import operator

# ======= Calculations =======

def mul(iterable):
    """
    Multiplies all of the values from an iterable.
    Similar to how sum() adds all of the values from an iterable.

    >>> mul([2,3])
    6
    >>> mul(xrange(1,6)) == math.factorial(5)
    True
    """

    return reduce(operator.mul, iterable, 1)

def comb(n, r):
    """
    Finds the number of combinations for n items taken r at a time.

    >>> comb(6, 6)
    1
    >>> comb(6, 1)
    6
    """
    return math.factorial(n) / (math.factorial(r)*(math.factorial(n-r)))

# ======= Iterators =======

class CachedIter(object):
    """ 
    Stores the output from an iterator so previously generated values can be accessed again.
    Useful for infinite series.
    
    >>> l = CachedIter(xrange(1,5))
    >>> l[2]
    3
    >>> l[:2]
    [1, 2]

    
    """

    def __init__(self, iterator):
        self._iter = iter(iterator)
        self.cache = []

    def __iter__(self):
        for iter_index in count(0):
            try:
                item = self.cache[iter_index]
            except IndexError:
                item = self.next()

            yield item

    def __getitem__(self, index):
        if isinstance(index, slice):
            return list(islice(iter(self), index.start, index.stop, index.step))
        else:
            return islice(iter(self), index, index+1).next()

    def next(self):
        n = self._iter.next()
        self.cache.append(n)
        return n

def fib():
    """ Simple generator for the fibonacci sequence """

    a, b = 1, 1
    for dummy in count():
        yield a
        a, b = b, a+b

def find_primes():
    """ Very naive generator for finding primes. """
    found_primes = []

    for v in count(2):
        for p in found_primes:
            if v % p == 0:
                break
        else:
            found_primes.append(v)
            yield v

# Some CachedIterators. Use these rather then the generator directly.
primes = CachedIter(find_primes())
fib_numbers = CachedIter(fib())

def find_triangle_numbers(start=0):
    """ Generates triangle numbers """
    val = sum(range(1,start))

    for i in count(start+1):
        yield val
        val += i

def find_prime_factors(n):
    """ Finds the prime factors of a positive integer n """
    
    while n > 1:
        for p in primes:
            if n % p == 0:
                yield p
                n /= p
                break

def find_divisors_from_primes(prime_factors):
    """ 
    Generates a set of divisors from a list of prime factors 
    
    >>> find_divisors_from_primes([2,2,3])
    set([1, 2, 3, 4, 6, 12])
    
    """

    divisors = set([1, mul(prime_factors)])

    return divisors.union(mul(vals) for vals in chain.from_iterable(combinations(prime_factors, r) for r in range(1, len(prime_factors))))

def find_divisors(n):
    """
    Generates a set of divisors from the number n 

    >>> find_divisors(12)
    set([1, 2, 3, 4, 6, 12])
    """
    return find_divisors_from_primes(list(find_prime_factors(n)))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
