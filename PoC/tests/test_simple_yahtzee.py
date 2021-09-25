import pytest
from pytest import approx
from ..simple_yahtzee import score, expected_value, gen_all_holds, strategy


@pytest.mark.parametrize(
    'hand, expected',
    [
        ((1,2,3), 3),
        ((1,1,2), 2),
        ((1,1,1), 3),
        ((6,6,6), 18),
        ((4,4,6), 8),
    ],
)
def test_score(hand, expected):
    assert score(hand) == expected


@pytest.mark.parametrize(
    'held, sides, nfree, expected',
    [
        ((1,2,), 6, 1, approx(4.0, rel=0.01)),
        ((6,6,), 6, 1, approx(13.0, rel=0.01)),
        ((5,5,5), 6, 2, approx(50./3, rel=0.01)),
        ((), 6, 1, approx(3.5, rel=0.01)),
        ((), 4, 1, approx(2.5, rel=0.01)),
        ((), 4, 2, approx(3.75, rel=0.01)),
        ((3,3), 8, 5, approx(11.3590087891, rel=0.01)),
    ],
)
def test_expected_value(held, sides, nfree, expected):
    assert expected_value(held, sides, nfree) == expected


@pytest.mark.parametrize(
    'hand, expected',
    [
        ((1,), 2),
        ((1,1), 3),
        ((2,3), 4),
        ((), 1),
        ((7,8,8,4), 12),
        ((5,5), 3),
    ],
)
def test_gen_all_holds_by_num(hand, expected):
    assert len(gen_all_holds(hand)) == expected


@pytest.mark.parametrize(
    'hand, expected',
    [
        ((1,), set([(), (1,)])),
        ((1,1), set([(), (1,), (1,1)])),
        ((2,3), set([(), (2,), (3,), (2,3)])),
        ((5,5), set([(5,), (), (5,5)])),
    ]
)
def test_gen_all_holds_by_exact_set(hand, expected):
    assert gen_all_holds(hand) == expected


@pytest.mark.parametrize(
    'hand, sides, expected',
    [
        ( (6,6,4), 6, [(approx(13.0, rel=0.01), (6,6))] ),
        ( (7,2), 8, [(approx(8.0, rel=0.01), (7,))] ),
        ( (1,), 6, [(approx(3.5, rel=0.01), ())]),
    ]
)
def test_strategy(hand, sides, expected):
    assert strategy(hand, sides) in expected

