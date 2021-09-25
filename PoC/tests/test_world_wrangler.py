import pytest
from ..word_wrangler import remove_duplicates, intersect, merge, merge_sort, gen_all_strings

@pytest.fixture
def word_case1():
    return 'aa'

@pytest.fixture
def word_case2():
    return 'aab'

@pytest.fixture
def word_case3():
    return ''

@pytest.fixture
def word_case4():
    return 'abc'

@pytest.fixture
def word_case5():
    return 'a'


def test_gen_all_strings_empty(word_case3):
    assert gen_all_strings(word_case3) == ['']

def test_gen_all_strings_one_letter(word_case5):
    word = word_case5
    assert gen_all_strings(word) == ['', word]

def test_gen_all_string_all_unique(word_case4):
    word = word_case4
    lst = gen_all_strings(word)
    assert len(lst) == 16

def test_gen_all_strings_has_duplicate(word_case2):
    word = word_case2
    lst = gen_all_strings(word)
    assert len(lst) == 16
    assert 'aa' in lst
    assert 'aba' in lst
    assert lst.count('aa') == 2
    assert lst.count('ab') == 2
    assert lst.count('ba') == 2

def test_gen_all_strings_small_has_duplicate(word_case1):
    word = word_case1
    lst = gen_all_strings(word)
    assert len(lst) == 5
    assert lst.count('aa') == 2


@pytest.fixture
def list_case1():
    return []

@pytest.fixture
def list_case2():
    return ['']

@pytest.fixture
def list_case3():
    return ['', 'aa', 'aaz', 'ab']

@pytest.fixture
def list_case4():
    return ['', 'a', 'ab', 'b', 'ba']

@pytest.fixture
def list_case5():
    return ['', 'a']

def test_merge_empties(list_case1):
    assert merge(list_case1, list_case1) == []

def test_merge_zero_length(list_case2, list_case5):
    assert merge(list_case2, list_case5) == ['', '', 'a']

def test_merge_random(list_case4, list_case3):
    lst1, lst2 = list_case3, list_case4
    new_lst = merge(lst1, lst2)
    assert new_lst == ['', '', 'a', 'aa', 'aaz', 'ab', 'ab', 'b', 'ba']

def test_merge_size(list_case1, list_case3):
    assert len(merge(list_case1, list_case3)) == 4

def test_merge_size2(list_case3, list_case4):
    lst1, lst2 = list_case3, list_case4
    new_lst = merge(lst1, lst2)
    assert len(new_lst) == 9

def test_merge_no_mutate(list_case5):
    lst1, lst2 = list_case5, list_case5
    _ = merge(lst1, lst2)
    assert lst1 == lst2 == ['', 'a']


@pytest.mark.parametrize(
    'lst, expected',
    [
        ([], []),
        ([''], ['']),
        (['a',''], ['','a']),
        (['a','','a'], ['','a','a']),
        (['ab','a','', 'b','ba'], ['','a','ab','b','ba']),
    ]
)
def test_merge_sort(lst, expected):
    assert merge_sort(lst) == expected


@pytest.mark.parametrize(
    'lst, expected',
    [
        ([], []),
        ([''], ['']),
        (['','a'], ['','a']),
        (['','a','a'], ['','a']),
        (['','a','aa','aa','b','b','ba','ba'], ['','a','aa','b','ba']),
    ]
)
def test_remove_duplicates(lst, expected):
    assert remove_duplicates(lst) == expected


def test_intersect_empties(list_case1):
    assert intersect(list_case1, list_case1) == []

def test_intersect_empties2(list_case1, list_case3):
    assert intersect(list_case1, list_case3) == []

def test_intersect_normal(list_case3, list_case4):
    assert intersect(list_case3, list_case4) == ['', 'ab']

def test_intersect_normal2(list_case4, list_case5):
    assert intersect(list_case4, list_case5) == ['', 'a']

def test_intersect_normal2(list_case5):
    assert intersect(list_case5, list_case5) == ['', 'a']

def test_intersect_no_mutate(list_case5):
    lst = list_case5
    _ = intersect(lst, lst)
    assert lst == ['', 'a']



