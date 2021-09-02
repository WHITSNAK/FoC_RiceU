"""
Monte Carlo Tic-Tac-Toe Machine Player
 that uses Monte Carlo method to sample
 the best move
"""

import random
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1000         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 2.0   # Score for squares played by the other player



def mc_trial(board, player):
    """
    Play a full TTT game with the given board settings 
     and the starting player, of course randomly for MC sampling
     
    parameter
    ---------
    board: TTTBoard object
    player: the player that is about to make a move
    
    return
    ------
    None: it directly modify the given 'board' instance
    """
    current_player = player
    while not board.check_win():
        empties = board.get_empty_squares()
        move = random.choice(empties)
        board.move(move[0], move[1], current_player)
        current_player = provided.switch_player(current_player)
    

def mc_update_scores(scores, board, player):
    """
    Given a finished game, update the MC trial scores

    parameter
    ---------
    scores: grid with the same size of board's dimension
    board: TTTBoard instance
    player: machine player code

    return
    ------
    None: directly modify the given 'scores' grid
    """
    dim = board.get_dim()
    
    winner = board.check_win()
    if winner == provided.DRAW:
        sign = 0
    elif winner == player:
        sign = 1
    else:
        sign = -1

    # loop through all squares in a grid
    for row_i in range(dim):
        for col_j in range(dim):
            val = board.square(row_i, col_j)

            if val == provided.EMPTY:
                scores[row_i][col_j] += 0
            else:
                # normally win +my_score, -other_score
                if val == player:
                    score = SCORE_CURRENT
                else:
                    score = -SCORE_OTHER

                # flip signs if loss, or just ignore if draw
                scores[row_i][col_j] += sign * score


def get_best_move(board, scores):
    """
    Assess a expected scores grid, choose the next best move
     given current board settings

    parameter
    ---------
    board: TTTBoard board instance
    scores: A grid of MC scores

    return
    ------
    (row, col)
    """
    if board.check_win():
        return None  # game is ended
    
    dim = board.get_dim()
    empties = set(board.get_empty_squares())

    # find the max score first
    max_score = float('-inf')
    for row_i in range(dim):
        for col_j in range(dim):
            val = scores[row_i][col_j]
            if (row_i, col_j) in empties:
                max_score = max(max_score, val)
    
    indices = []
    # loop through again to find idices
    for row_i in range(dim):
        for col_j in range(dim):
            val = scores[row_i][col_j]
            idx = (row_i, col_j)
            if val == max_score and idx in empties:
                indices.append(idx)
    
    # if more than one, just randomly choose one
    return random.choice(indices)


def mc_move(board, player, trials):
    """
    Monte Carlo Simulated best move

    parameter
    ---------
    board: TTTBoard instance for the current game
    player: the machine player
    trials: number of times to do the MC simulation

    return
    ------
    (row, column): index for the move in a grid
    """
    dim = board.get_dim()
    scores = [[0]*dim for _ in range(dim)]
    
    for _ in range(trials):
        board2 = board.clone()
        mc_trial(board2, player)
        mc_update_scores(scores, board2, player)
    
    move = get_best_move(board, scores)
    return move



# self plays
# provided.play_game(mc_move, NTRIALS, False)        

# GUI interactive plays
# import poc_ttt_gui
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
