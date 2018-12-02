from itertools import count

import pytest

from euler_tools import AscendingCachedIter, CachedIter


def test_cachediter_infinite():
    evens = CachedIter(count(2, 2))

    assert evens[1] == 4
    assert evens[:2] == [2, 4]
    assert evens[2:5] == [6, 8, 10]
    assert evens[5:15:2] == [12, 16, 20, 24, 28]

    evens_sliced = evens[5:]
    assert isinstance(evens_sliced, CachedIter)
    assert evens_sliced[:2] == [12, 14]


def test_cachediter_multiple_iter():
    """
    Multiple iterators on the same CachedIter don't affect each other
    """
    evens = CachedIter(count(2, 2))

    i1 = iter(evens)
    i2 = iter(evens)

    assert next(i1) == 2
    assert next(i2) == 2
    assert next(i1) == 4
    assert next(i2) == 4


def test_ascendingcachediter_finite():
    finite = AscendingCachedIter(range(1, 10))

    assert 2 in finite
    assert -3 not in finite
    assert 20 not in finite


def test_ascendingcachediter_infinte():
    evens = AscendingCachedIter(count(2, 2))

    assert 2 in evens
    assert 3 not in evens


def test_ascendingcachediter_index():
    evens = AscendingCachedIter(count(2, 2))

    assert evens[4] == 10
    assert evens.index(10) == 4

    with pytest.raises(ValueError):
        evens.index(3)
