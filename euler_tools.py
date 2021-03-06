import operator
from collections.abc import Container, Iterable
from functools import reduce, wraps
from itertools import chain, combinations, compress, count, cycle, islice
from math import factorial, sqrt

__all__ = (
    "get_digits",
    "concat",
    "product",
    "comb",
    "all_combos",
    "powerset",
    "CachedIter",
    "AscendingCachedIter",
    "fib",
    "eratos",
    "fib_num",
    "find_triangle_numbers",
    "find_prime_factors",
    "find_divisors_from_primes",
    "find_divisors",
    "is_square",
)


# ======= Calculations =======


def get_digits(num):
    return set(str(num))


def concat(iterable):
    return u"".join(str(v) for v in iterable)


def product(iterable):
    """
    Multiplies all of the values from an iterable.
    Similar to how sum() adds all of the values from an iterable.

    >>> product([2,3])
    6
    >>> product(range(1,6)) == factorial(5)
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
    return factorial(n) // (factorial(r) * (factorial(n - r)))


def all_combos(s):
    """ 
    Generates tuples of all possible combinations of the items in s.

    >>> combos = list(all_combos([2,2,3]))
    >>> (2, 2) in combos
    True
    >>> (2,) in combos
    True
    """

    return chain.from_iterable(
        (tuple(c) for c in combinations(s, r)) for r in range(1, len(s) + 1)
    )


def powerset(s):
    """
    Creates a set of all possible subsets of s except for the empty set.
    >>> p_set = powerset([1,2,3])
    >>> {1,2,3} in p_set
    True
    >>> {1,3} in p_set
    True
    >>> {2,} in p_set
    True
    """

    return frozenset(frozenset(c) for c in all_combos(s))


# ======= Iterators =======


class CachedIter(Iterable, object):
    """ 
    Stores the output from an iterator so previously generated values can be accessed again.
    Supports indexing and slicing. Useful for infinite series.
    
    >>> from itertools import count
    >>> evens = CachedIter(count(2,2))

    Supports indexing
    >>> evens[1]
    4

    And slicing
    >>> list(evens[:2])
    [2, 4]
    >>> list(evens[2:5])
    [6, 8, 10]

    And slicing those slices
    >>> evens_sliced = evens[5:]
    >>> list(evens_sliced[:2])
    [12, 14]
    """

    def __init__(self, iterable):
        self._iter = iter(iterable)
        self.cache = []

    def __iter__(self):
        for idx in count():
            try:
                yield self.cache[idx]
            except IndexError:
                yield next(self)

    def __getitem__(self, index):
        if isinstance(index, slice):
            s = islice(iter(self), index.start, index.stop, index.step)
            if index.stop:
                return list(s)
            else:
                return self.__class__(s)
        else:
            if index < 0:
                raise IndexError(
                    "{0} does not support negative indicies".format(
                        self.__class__.__name__
                    )
                )

            return next(islice(iter(self), index, index + 1))

    def __next__(self):
        n = next(self._iter)
        self.cache.append(n)
        return n


class AscendingCachedIter(CachedIter, Container):
    """
    A CachedIter for infinite sequences that are ascending, every value in the sequence 
    is greater or equal to all previous values. These properties allow for checking if 
    it contains a value w/o running into an infinite loop for values not in the sequence. 
    This only holds true if the sequence is finite or if the value being checked is inside 
    the range of the sequence.

    >>> evens = AscendingCachedIter(count(2, 2))
    >>> 10 in evens
    True
    >>> 11 in evens
    False

    >>> evens.index(10)
    4
    >>> evens[4]
    10
    >>> evens.index(11)
    Traceback (most recent call last):
        ...
    ValueError: 11 is not in AscendingCachedIter

    """

    def __contains__(self, item):
        try:
            self.index(item)
            return True
        except (ValueError, StopIteration):
            return False

    def index(self, item):
        if self.cache:
            try:
                return self.cache.index(item)
            except ValueError:
                next_val = self.cache[-1]
        else:
            next_val = None

        idx = len(self.cache)
        while next_val is None or item > next_val:
            next_val = next(self)

            if item == next_val:
                return idx

            idx += 1

        raise ValueError("{0} is not in {1}".format(item, self.__class__.__name__))


def fib():
    """ Simple nieve generator for the fibonacci sequence """

    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b


def eratos():
    """ Prime number generator using sieve of eratos """
    D = {9: 3, 25: 5}  # composite num -> 1st prime factor
    yield 2
    yield 3
    yield 5
    MASK = (1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0)
    MODULOS = frozenset((1, 7, 11, 13, 17, 19, 23, 29))

    for q in compress(count(7, 2), cycle(MASK)):  # 235 wheel
        p = D.pop(q, None)
        if p is None:
            D[q * q] = q
            yield q
        else:
            x = q + 2 * p
            while x in D or (x % 30) not in MODULOS:
                x += 2 * p
            D[x] = p


# Cached iter of primes used by other functions in this module.
primes = AscendingCachedIter(eratos())


def fib_num(idx):
    """ Finds the fibonacci number at a given index """
    gold_ratio = (1 + sqrt(5)) / 2
    return int((gold_ratio ** idx - (1 - gold_ratio) ** idx) / sqrt(5))


def find_triangle_numbers(start=0):
    """ Generates triangle numbers """
    val = sum(range(1, start))

    for i in count(start + 1):
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
    
    >>> divisors = find_divisors_from_primes([2,2,3])
    >>> sorted(divisors)
    [1, 2, 3, 4, 6, 12]
    
    """

    return {1} | set(product(vals) for vals in all_combos(prime_factors))


def find_divisors(n):
    """
    Generates a set of divisors from the number n 

    >>> divisors = find_divisors(12)
    >>> sorted(divisors)
    [1, 2, 3, 4, 6, 12]
    """
    return find_divisors_from_primes(list(find_prime_factors(n)))


def is_square(k):
    return int(sqrt(k)) ** 2 == int(k)
