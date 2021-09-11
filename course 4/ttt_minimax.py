"""
Mini-max Tic-Tac-Toe Player
"""
# import poc_ttt_gui
import poc_ttt_provided as provided

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}


def _opponent_move(board, opp):
    """
    Generate a list of counter scores for mini operations

    parameter
    ---------
    board: the state of game
    opp: opponent player that is deciding the move

    return
    ------
    best score
    """
    winner = board.check_win()
    if winner is not None:  # leaf nodes
        board_score = SCORES[winner]
        return board_score  # does not flip sign here

    # not leaf nodes
    best_score = float('-inf')
    for pos_move in board.get_empty_squares():
        tmp_board = board.clone()
        tmp_board.move(pos_move[0], pos_move[1], opp)
        score = _opponent_move(tmp_board, provided.switch_player(opp))
        # uniform for X and O all to max on mini
        best_score = max(best_score, score * SCORES[opp])

        # early termination, 1 is the best score
        if best_score == 1:
            break
    return best_score * SCORES[opp]  # convert back to correct board score


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
        mini_score = _opponent_move(tmp_board, provided.switch_player(player))
        mini_scores.append((mini_score, pos_move))
    
    # Best move -> max for X == +1, max for O == -1
    res = max(mini_scores, key=lambda x: x[0] * SCORES[player])
    return res

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
