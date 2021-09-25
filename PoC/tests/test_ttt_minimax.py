import pytest
from ..poc_ttt_provided import TTTBoard, PLAYERO, PLAYERX, EMPTY
from ..ttt_minimax import mm_move, _opponent_move

O, X, E = PLAYERO, PLAYERX, EMPTY


@pytest.fixture
def game_state1():
    _board = [
        [O,X,E],
        [O,X,E],
        [E,O,X]
    ]
    return TTTBoard(3, board=_board)

@pytest.fixture
def game_state2():
    _board = [
        [O,X,E],
        [O,X,E],
        [X,O,X]
    ]
    return TTTBoard(3, board=_board)

@pytest.fixture
def game_state3():
    _board = [
        [O,X,E],
        [O,X,O],
        [X,O,X]
    ]
    return TTTBoard(3, board=_board)

@pytest.fixture
def game_state4():
    _board = [
        [O,X,X],
        [O,X,O],
        [X,O,X]
    ]
    return TTTBoard(3, board=_board)

@pytest.fixture
def game_state5():
    _board = [
        [O,X,E],
        [O,X,X],
        [E,O,X]
    ]
    return TTTBoard(3, board=_board)

@pytest.fixture
def game_state6():
    _board = [
        [X,X,O],
        [E,X,X],
        [O,E,O]
    ]
    return TTTBoard(3, board=_board)


def test_opp_move_full(game_state4):
    assert _opponent_move(game_state4, X) == 1
    assert _opponent_move(game_state4, O) == 1

def test_opp_move_1step(game_state3):
    assert _opponent_move(game_state3, X) == 1
    assert _opponent_move(game_state3, O) == 0

def test_opp_move_2step(game_state2):
    assert _opponent_move(game_state2, O) == 0

def test_opp_move_2step2(game_state5):
    assert _opponent_move(game_state5, O) == -1

def test_mm_move_3step(game_state1):
    assert mm_move(game_state1, X) == (0, (2, 0))

def test_mm_move_2step_winning_move_O(game_state5):
    assert mm_move(game_state5, O) == (-1, (2, 0))

def test_mm_move_2step_winning_move_O2(game_state6):
    assert mm_move(game_state6, O) == (-1, (2,1))

