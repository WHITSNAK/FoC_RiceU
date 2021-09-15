"""
Student facing implement of solitaire version of Mancala - Tchoukaillon

Goal: Move as many seeds from given houses into the store

In GUI, you make ask computer AI to make move or click to attempt a legal move
"""

class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """
    
    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        self._board = [0]
       
    def __str__(self):
        """
        Return string representation for Mancala board
        in the form of left to right -> ... H3 H2 H1 | Store
        """
        lst = [str(n) for n in reversed(self._board)]
        return '[' + ', '.join(lst) + ']'
    
    def get_board(self):
        return self._board
    
    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        in the form of -> Store | H1 H2 H3 ...
        """
        self._board = list(configuration)
    
    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        return self._board[house_num]
    
    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        """
        i, n = house_num, self.get_num_seeds(house_num)
        if i == 0 or n == 0:
            return False
        return n == i
    
    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        if not self.is_legal_move(house_num):
            return
        
        for i in range(house_num):
            self._board[i] += 1
        self._board[house_num] = 0
    
    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        i = 0
        for _i in range(1, len(self._board)):
            if self.is_legal_move(_i):
                return _i
        return i
    
    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        return sum(self._board[1:]) == 0
    
    def plan_moves(self):
        """
        Return a sequence (list) of legal moves based on the following heuristic: 
        After each move, move the seeds in the house closest to the store 
        when given a choice of legal moves
        Not used in GUI version, only for machine testing
        """
        copy_me = SolitaireMancala()
        copy_me.set_board(list(self._board))
        
        moves = []
        i = copy_me.choose_move()
        while i != 0:
            moves.append(i)
            copy_me.apply_move(i)
            i = copy_me.choose_move()
        return moves
    

    
import poc_simpletest

def run_suite(game_class):
    suite = poc_simpletest.TestSuite()
    
    game = game_class()
    suite.run_test(game._board, [0], 'Test 1.0')
    
    config1 = [0,0,1,1,3,5,0]
    game.set_board(config1)
    suite.run_test(game.get_board(), [0,0,1,1,3,5,0], 'Test 1.1')
    suite.run_test(str(game), '[0, 5, 3, 1, 1, 0, 0]', 'Test 1.2')
    suite.run_test(game.get_num_seeds(0), 0, 'Test 1.3')
    suite.run_test(game.get_num_seeds(1), 0, 'Test 1.4')
    suite.run_test(game.get_num_seeds(5), 5, 'Test 1.5')
    suite.run_test(game.is_legal_move(0), False, 'Test 1.6')
    suite.run_test(game.is_legal_move(2), False, 'Test 1.7')
    suite.run_test(game.is_legal_move(5), True, 'Test 1.8')
    
    move = game.choose_move()
    suite.run_test(move, 5, 'Test 1.9')
    game.apply_move(move)
    suite.run_test(game.get_board(), [1,1,2,2,4,0,0], 'Test 1.10')
    
    move = game.choose_move()
    suite.run_test(move, 1, 'Test 1.11')
    game.apply_move(move)
    suite.run_test(game.get_board(), [2,0,2,2,4,0,0], 'Test 1.12')
    
    move = game.choose_move()
    suite.run_test(move, 2, 'Test 1.13')
    game.apply_move(move)
    suite.run_test(game.get_board(), [3,1,0,2,4,0,0], 'Test 1.14')
    
    correct_moves = game.plan_moves()
    suite.run_test(correct_moves, [1,4,1,3,1,2,1], 'Test 1.15')
    
    for m in correct_moves:
        game.apply_move(m)
    suite.run_test(game.is_game_won(), True, 'Test 1.16')
    
    suite.report_results()

# unittests
#run_suite(SolitaireMancala)
    
# Import GUI code once you feel your code is correct
#import poc_mancala_gui
#poc_mancala_gui.run_gui(SolitaireMancala())

