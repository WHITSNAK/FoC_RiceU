import pytest
from alignment import build_scoring_matrix, create_matrix, compute_alignment_matrix


@pytest.mark.parametrize(
    'alph, diag_s, odiag_s, dash_s, expected',
    [
        ({'c','a','t','d','d'}, 10, 2, -5,
         {'a': {'a': 10, 'c':  2, 'd':  2, 't':  2, '-': -5},
          'c': {'a':  2, 'c': 10, 'd':  2, 't':  2, '-': -5},
          'd': {'a':  2, 'c':  2, 'd': 10, 't':  2, '-': -5},
          't': {'a':  2, 'c':  2, 'd':  2, 't': 10, '-': -5},
          '-': {'a': -5, 'c': -5, 'd': -5, 't': -5, '-': -5}}),
        ({'a','b','c','-'}, 0, 5, -100,
         {'a': {'a': 0, 'b': 5, 'c': 5, '-': -100},
          'b': {'a': 5, 'b': 0, 'c': 5, '-': -100},
          'c': {'a': 5, 'b': 5, 'c': 0, '-': -100},
          '-': {'a': -100, 'b': -100, 'c': -100, '-': -100}}),
        (set([]), 100, 100, -100, {'-': {'-': -100}}),
    ]
)
def test_build_scoring_matrix(alph, diag_s, odiag_s, dash_s, expected):
    matrix = build_scoring_matrix(alph, diag_s, odiag_s, dash_s)
    assert matrix == expected


@pytest.mark.parametrize(
    'nrow, ncol, default, expected',
    [
        (0,10,0, []),
        (1,2,10, [[10, 10]]),
        (2,3,5, [[5,5,5],[5,5,5]]),
    ]
)
def test_create_matrix(nrow, ncol, default, expected):
    assert create_matrix(nrow, ncol, default) == expected



@pytest.mark.parametrize(
    'seq_x, seq_y, scores, global_flag, expected',
    [
        ('AA', 'TAAT',
         build_scoring_matrix(set(['A','T']), 10, 4, -6), True,
         [[  0, -6,-12,-18,-24],
          [ -6,  4,  4, -2, -8],
          [-12, -2, 14, 14,  8]]
        ),
        ('AA', 'TAAT',
         build_scoring_matrix(set(['A','T']), 10, 4, -6), False,
         [[ 0, 0, 0, 0, 0],
          [ 0, 4,10,10, 4],
          [ 0, 4,14,20,14]]
        ),
    ]
)
def test_compute_alignment_matrix(seq_x, seq_y, scores, global_flag, expected):
    assert compute_alignment_matrix(seq_x, seq_y, scores, global_flag) == expected


