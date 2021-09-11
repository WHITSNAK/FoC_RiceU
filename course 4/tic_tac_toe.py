# %%
"""
Mini-max Tic-Tac-Toe Player
"""

# import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
# import codeskulptor
# codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

STATE_MAP = {
    2: 'X win', 3: 'O win', 4: 'Draw', None: 'Not Over'
}
PLAYER_MAP = {
    2: 'Player X', 3: 'Player O', 4:'Draw',
}

def _opponent_move(board, opp):
    winner = board.check_win()
    if winner is not None:  # leaf nodes
        return SCORES[winner]  # does not flip sign here

    # not leaf nodes
    min_score = float('inf')
    for pos_move in board.get_empty_squares():
        tmp_board = board.clone()
        tmp_board.move(pos_move[0], pos_move[1], opp)
        score = _opponent_move(tmp_board, provided.switch_player(opp))
        min_score = min(min_score, score)
    return min_score


def mm_move(board, player):
    """
    Make a move on the board.
    
    parameter
    ---------
    board: the current board setting
    player: the player that is going to move next

    return
    ------
    score, move -> int, (row_i, col_j)
    """
    mini_scores = []
    for pos_move in board.get_empty_squares():
        tmp_board = board.clone()
        tmp_board.move(pos_move[0], pos_move[1], player)
        score = _opponent_move(tmp_board, provided.switch_player(player))
        score *= SCORES[player]  # uniform for X and O all to max on mini
        mini_scores.append((score, pos_move))
    
    # print mini_scores
    return max(mini_scores, key=lambda x: x[0])

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]


# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


# %%
from poc_ttt_provided import TTTBoard, PLAYERO, PLAYERX, EMPTY

O, X, E = PLAYERO, PLAYERX, EMPTY

_board = [
    [O,X,E],
    [O,X,E],
    [X,O,X]
]
board = TTTBoard(3, board=_board)
# print board
# board.move(0,2,X)
# print board
# board.move(2,0,O)
# print board
# print board.check_win()
mm_move(board, O)
