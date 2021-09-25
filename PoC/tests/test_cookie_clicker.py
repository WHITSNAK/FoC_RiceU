import pytest
from pytest import approx
from ..cookie_clicker import ClickerState, simulate_clicker
from ..cookie_clicker import strategy_cursor_broken, strategy_none, strategy_polar
from ..poc_clicker_provided import BuildInfo


# clickerstart tests
def test_clickerstate_init_get():
    state = ClickerState()
    assert state._total_cookies == 0.0
    assert state.get_cookies() == 0.0
    assert state.get_time() == 0.0
    assert state.get_cps() == 1.0
    assert len(state.get_history()) == 1
    assert len(state.get_history()[0]) == 4
    assert type(state._builds_counter) is dict
    assert len(state._builds_counter) == 0


@pytest.mark.parametrize(
    'cookies_needed, cur_cookies, cps, expected',
    [
        (12.5, 0.0, 1.0, 13.0),
        (100, 20.0, 3.0, 27.0),
        (50, 100, 3.0, 0.0),
    ],
)
def test_clickerstate_time_until(cookies_needed, cur_cookies, cps, expected):
    state = ClickerState()
    state._cookies = cur_cookies
    state._cps = cps

    res = state.time_until(cookies_needed)
    assert type(res) is float
    assert res == approx(expected, rel=1e-4)


@pytest.mark.parametrize(
    'time, cps, old_data, new_data',
    [   # data -> time, total_cookies, current_cookies
        (10.0, 1.0, (0.0, 0.0, 0.0), (10.0, 10.0, 10.0)),
        (0.0, 1.0, (5.0, 5.0, 6.0), (5.0, 5.0, 6.0)),
    ],
)
def test_clickerstate_wait(time, cps, old_data, new_data):
    state = ClickerState()
    state._time = old_data[0]
    state._total_cookies = old_data[1]
    state._cookies = old_data[2]
    state._cps = cps

    state.wait(time)
    assert state._time == new_data[0]
    assert state._total_cookies == new_data[1]
    assert state._cookies == new_data[2]


@pytest.mark.parametrize(
    'item_name, cost, additional_cps, expected',
    [   # expected -> (current_cookies, cps)
        ('A', 100.0, 0.2, (9900.0, 5.2)),
        ('B', 9999.0, 100.5, (1.0, 105.5)),
    ],
)
def test_clickstate_buy_item_has_money(item_name, cost, additional_cps, expected):
    state = ClickerState()
    state._cookies = 10000.0
    state._cps = 5.0
    state.buy_item(item_name, cost, additional_cps)

    assert state._cookies == expected[0]
    assert state._cps == expected[1]
    assert len(state._history) == 2
    assert item_name in state._history[-1]
    assert state._builds_counter[item_name] == 1


@pytest.mark.parametrize(
    'item_name, cost, additional_cps, expected',
    [   # expected -> (current_cookies, cps)
        ('A', 100.0, 0.2, (50.0, 5.0)),
        ('B', 9999.0, 100.5, (50.0, 5.0)),
    ],
)
def test_clickstate_buy_item_no_money(item_name, cost, additional_cps, expected):
    state = ClickerState()
    state._cookies = 50.0
    state._cps = 5.0
    state.buy_item(item_name, cost, additional_cps)

    assert state._cookies == expected[0]
    assert state._cps == expected[1]
    assert len(state._history) == 1
    assert len(state._builds_counter) == 0


# strategies tests
build_info = {
    "Cursor": [15.0, 0.1],
    "Grandma": [100.0, 0.5],
}

@pytest.mark.parametrize(
    'args, expected',
    [
        ([0, 1, [], 30, BuildInfo(build_info)], 'Cursor'),
        ([0, 1, [], 14, BuildInfo(build_info)], None),
        ([10, 1, [], 4, BuildInfo(build_info)], None),
    ]
)
def test_stgy_cursor(args, expected):
    assert strategy_cursor_broken(*args) == expected


@pytest.mark.parametrize(
    'args, expected',
    [
        ([0, 1, [], 30, BuildInfo(build_info)], None),
        ([0, 1, [], 15, BuildInfo(build_info)], None),
        ([10, 1, [], 5, BuildInfo(build_info)], None),
    ]
)
def test_stgy_none(args, expected):
    assert strategy_none(*args) == expected


build_info1 = {
    "Cursor": [15.0, 0.1],
    "Grandma": [100.0, 0.5],
}

build_info2 = {
    "Cursor": [150.0, 0.1],
    "Grandma": [100.0, 0.5],
}
build_info3 = {'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}

@pytest.mark.parametrize(
    'args, expected',
    [
        ([0.0, 1.0, [], 30.0, BuildInfo(build_info1), 'low'], 'Cursor'),
        ([150., 1.0, [], 30.0, BuildInfo(build_info1), 'low'], 'Cursor'),
        ([0.0, 1.0, [], 14.0, BuildInfo(build_info1), 'low'], None),
        ([10.0, 1.0, [], 4.0, BuildInfo(build_info1), 'low'], None),
        ([0.0, 1.0, [], 200.0, BuildInfo(build_info2), 'low'], 'Grandma'),
        ([150.0, 1.0, [], 30.0, BuildInfo(build_info2), 'low'], 'Grandma'),
        ([0.0, 1.0, [(0.0, None, 0.0, 0.0)], 50000.0, BuildInfo(build_info3), 'low'], 'A')
    ],
)
def test_stgy_polar_lowest(args, expected):
    assert strategy_polar(*args) == expected


@pytest.mark.parametrize(
    'args, expected',
    [
        ([0, 1, [], 30, BuildInfo(build_info1), 'high'], 'Cursor'),
        ([150, 1, [], 30, BuildInfo(build_info1), 'high'], 'Grandma'),
        ([0, 1, [], 14, BuildInfo(build_info1), 'high'], None),
        ([10, 1, [], 4, BuildInfo(build_info1), 'high'], None),
        ([0, 1, [], 200, BuildInfo(build_info2), 'high'], 'Cursor'),
        ([150, 1, [], 30, BuildInfo(build_info2), 'high'], 'Cursor'),
        ([0.0, 1.0, [(0.0, None, 0.0, 0.0)], 500.0, BuildInfo(build_info3), 'high'], 'B')
    ],
)
def test_stgy_polar_highest(args, expected):
    assert strategy_polar(*args) == expected


# simulation tests
build_info1 = {
    "Cursor": [15.0, 0.1],
    "Grandma": [100.0, 0.5],
}
build_info2 = {
    "A": [10.0, 0.1],
    "B": [100.0, 0.5],
    'C': [150.0, 0.75],
}
build_info3 = {'Cursor': [15.0, 0.1]}
build_info4 = {'Cursor': [15.0, 50]}

@pytest.mark.parametrize(
    'args, expected',
    [
        ([BuildInfo(build_info1), 20, strategy_cursor_broken],
         '<Time=20.0, Total Cookies=20.5, Current Cookies=5.5, CPS=1.1>'),
        ([BuildInfo(build_info2), 100, strategy_none],
         '<Time=1e+02, Total Cookies=1e+02, Current Cookies=1e+02, CPS=1.0>'),
        ([BuildInfo(build_info3), 10, strategy_cursor_broken],
         '<Time=10.0, Total Cookies=10.0, Current Cookies=10.0, CPS=1.0>'),
        ([BuildInfo(build_info4), 16, strategy_cursor_broken],
         '<Time=16.0, Total Cookies=66.0, Current Cookies=13.9, CPS=1.51e+02>'),
        ([BuildInfo(build_info4), 0, strategy_cursor_broken],
         '<Time=0.0, Total Cookies=0.0, Current Cookies=0.0, CPS=1.0>'),
    ]
)
def test_simulation(args, expected):
    assert str(simulate_clicker(*args)) == expected