from tic_tac_toe import mc_trial, mc_update_scores, get_best_move
from tic_tac_toe import SCORE_CURRENT, SCORE_OTHER
from poc_ttt_provided import TTTBoard, EMPTY, PLAYERX, PLAYERO, DRAW
from .utils import compare_grid

E, X, O = EMPTY, PLAYERX, PLAYERO
SC, SO = SCORE_CURRENT, SCORE_OTHER


def test_mc_trail():
    stream = [
        {
            'board': [[X,X,O], [O,X,X],[E,E,O]],
            'player': O, 'expected': (DRAW, X),
        },
        {
            'board': [[O,X,O],[X,X,O],[X,E,E]],
            'player': O, 'expected': (DRAW, O),
        },
        {
            'board': [[O,X,X],[O,O,X],[X,O,E]],
            'player': O, 'expected': (O, ),
        },
        {
            'board': [[O,X,X],[O,O,X],[X,O,E]],
            'player': X, 'expected': (X, ),
        },
        {
            'board': [[E,X,O],[O,X,X],[E,O,E]],
            'player': X, 'expected': (X, DRAW),
        },
    ]
    for data in stream:
        results = set()
        for _ in range(100):
            board = TTTBoard(dim=3, board=data['board'])
            mc_trial(board, data['player'])
            results.add(board.check_win())
        
        assert None not in results
        for item in results:
            assert item in data['expected']


def test_mc_update_scores(mocker):
    # mock up for different values of two scores
    # to make distinction
    mocker.patch('PoC.tic_tac_toe.SCORE_CURRENT', 1.0)
    mocker.patch('PoC.tic_tac_toe.SCORE_OTHER', 2.0)
    SC, SO = 1.0, 2.0

    stream = [
        {
            'board': [[X,X,O], [O,X,X], [X,O,O]],
            'scores': [[0,0,0], [0,0,0], [0,0,0]],
            'player': O,  # draw
            'expected': [[0,0,0], [0,0,0], [0,0,0]],
        },
        {
            'board': [[X,X,O], [O,X,X], [O,X,O]],
            'scores': [[5,5,5], [3,3,3], [4,4,4]],
            'player': O,  # loss
            'expected': [[5+SO,5+SO,5-SC], [3-SC,3+SO,3+SO], [4-SC,4+SO,4-SC]],
        },
        {
            'board': [[X,X,O], [O,X,X], [O,X,O]],
            'scores': [[5,5,5], [3,3,3], [4,4,4]],
            'player': X,  # win
            'expected': [[5+SC,5+SC,5-SO], [3-SO,3+SC,3+SC], [4-SO,4+SC,4-SO]],
        },
        {
            'board': [[O,X,X],[O,O,X],[X,O,O]],
            'scores': [[2,2,2], [0,5,2.1], [1.5,1.5,3]],
            'player': O,  # win
            'expected': [[2+SC,2-SO,2-SO], [0+SC,5+SC,2.1-SO], [1.5-SO,1.5+SC,3+SC]],
        },
        {
            'board': [[O,X,X],[O,O,X],[X,O,O]],
            'scores': [[0,0,0], [0,0,0], [0,0,0]],
            'expected': [[SO,-SC,-SC], [SO,SO,-SC], [-SC,SO,SO]],
            'player': X,  # loss
        },
        {
            'board': [[X,E,O],[E,X,O],[X,E,O]],
            'scores': [[-3,-5,3], [-1,-5,-10], [0,0,0]],  # we can also have negative scores
            'expected': [[-3-SC,-5,3+SO], [-1,-5-SC,-10+SO], [0-SC,0,0+SO]],
            'player': X,  # loss
        },
        {
            'board': [[X,E,O],[E,X,O],[X,E,O]],
            'scores': [[0,0,0], [0,0,0], [0,0,0]],
            'expected': [[-SO,0,SC], [0,-SO,SC], [-SO,0,SC]],
            'player': O,  # win
        },
    ]
    
    for data in stream:
        board = TTTBoard(3, board=data['board'])
        scores = data['scores']
        expected_scores = data['expected']
        player = data['player']

        mc_update_scores(scores, board, player)

        print board, scores, expected_scores, player
        assert len(compare_grid(scores, expected_scores)) == 0


def test_get_best_move():
    stream = [
        {
            'board': [[E,E,E], [E,X,E], [E,E,E]],  # just started
            'scores': [[10,0,0], [0,0,0], [10,0,10]],
            'expected': [(0,0),(2,0),(2,2)],
        },
        {
            'board': [[O,X,X], [O,O,X], [X,O,X]],  # X Win no more move
            'scores': [[10,8,9], [1,2,3], [10,4,10]],
            'expected': [None],
        },
        {
            'board': [[O,O,X], [E,X,E], [O,E,X]],  # just started
            'scores': [[100,0,0], [10,500,5], [10,10,10]],
            'expected': [(1,0),(2,1)],
        },
        {
            'board': [[O,O,X], [E,X,E], [O,E,X]],  # just started
            'scores': [[100,0,0], [10,500,5], [10,10,10]],
            'expected': [(1,0),(2,1)],
        },
        {   # sometime, we have to choose within all negative numbers
            'board': [[X,X,E], [X,X,O], [O,E,O]],  
            'scores': [[-3,6,-2], [8,0,-3], [3,-2,-4]],
            'expected': [(0,2),(2,1)],
        },
    ]

    for data in stream:
        board = TTTBoard(3, board=data['board'])
        scores = data['scores']
        expected = data['expected']

        results = set()
        for _ in range(100):
            move = get_best_move(board, scores)
            results.add(move)
        
        for result in results:
            assert result in expected
