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
    >>> mul([2,3])
    6
    >>> mul(xrange(1,6)) == math.factorial(5)
    True
    """

    return reduce(operator.mul, iterable, 1)

def comb(n, r):
    """ Finds the number of combinations from n items taken r at a time """
    return math.factorial(n) / (math.factorial(r)*(math.factorial(n-r)))

# ======= Iterators =======

class CachedIter(object):
    """ Caches the output from an iterator """

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
    a, b = 1, 1
    for dummy in count():
        yield a
        a, b = b, a+b

def find_primes():
    found_primes = []

    for v in count(2):
        for p in found_primes:
            if v % p == 0:
                break
        else:
            found_primes.append(v)
            yield v

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

def find_divisors_from_primes(prime_divisors):
    """ Generates a set of divisors from a list of prime divisors """

    divisors = set([1, mul(prime_divisors)])

    return divisors.union(mul(vals) for vals in chain.from_iterable(combinations(prime_divisors, r) for r in range(1, len(prime_divisors))))

def find_divisors(n):
    return find_divisors_from_primes(list(find_prime_factors(n)))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
