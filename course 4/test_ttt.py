import pytest
from poc_ttt_provided import TTTBoard, PLAYERO, PLAYERX, EMPTY
from tic_tac_toe import mm_move, _opponent_move

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


def test_opp_move_full(game_state4):
    assert _opponent_move(game_state4, X) == 1
    assert _opponent_move(game_state4, O) == 1
