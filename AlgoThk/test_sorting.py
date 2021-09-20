import pytest
from sorting import count_inversion, merge


def test_count_inversion():
    lst = [5,4,3,6,7]
    assert lst == [5,4,3,6,7]
    assert count_inversion(lst) == 3
    # inplace
    assert lst == [3,4,5,6,7]

def test_count_inversion_empty():
    lst = []
    assert count_inversion(lst) == 0
    assert lst == []


def test_merge():
    a = [1, 4, 2, 3]
    b = a[:len(a)//2]
    c = a[len(a)//2:]

    assert merge(b, c, a) == 2
    assert a == [1,2,3,4]
