# %%
class SolitaireMancala:
    """
    Simple class that implements Solitaire Mancala
    """
    
    def __init__(self):
        """
        Create Mancala game with empty store and no houses
        """
        self._board = [0]
    
    def set_board(self, configuration):
        """
        Take the list configuration of initial number of seeds for given houses
        house zero corresponds to the store and is on right
        houses are number in ascending order from right to left
        """
        self._board = list(configuration)
    
    def __str__(self):
        """
        Return string representation for Mancala board
        """
        temp = list(self._board)
        temp.reverse()
        return str(temp)
    
    def get_num_seeds(self, house_num):
        """
        Return the number of seeds in given house on board
        """
        return self._board[house_num]

    def is_game_won(self):
        """
        Check to see if all houses but house zero are empty
        """
        for idx in range(1, len(self._board)):
            if self._board[idx] != 0:
                return False
        return True
    
    def is_legal_move(self, house_num):
        """
        Check whether a given move is legal
        """
        move_in_range = 0 < house_num < len(self._board)
        index_matches = self._board[house_num] == house_num
        return move_in_range and index_matches

    
    def apply_move(self, house_num):
        """
        Move all of the stones from house to lower/left houses
        Last seed must be played in the store (house zero)
        """
        if self.is_legal_move(house_num):  
            for idx in range(house_num):
                self._board[idx] += 1
            self._board[house_num] = 0

    def choose_move(self):
        """
        Return the house for the next shortest legal move
        Shortest means legal move from house closest to store
        Note that using a longer legal move would make smaller illegal
        If no legal move, return house zero
        """
        for house_num in range(1, len(self._board)):
            if self.is_legal_move(house_num):
                return house_num
        return 0
    
    def plan_moves(self):
        """
        Return a sequence (list) of legal moves based on the following heuristic: 
        After each move, move the seeds in the house closest to the store 
        when given a choice of legal moves
        Not used in GUI version, only for machine testing
        """
        new_board = SolitaireMancala()
        new_board.set_board(self._board)
        move_list = []
        next_move =  new_board.choose_move()
        while next_move != 0:
            new_board.apply_move(next_move)
            move_list.append(next_move)
            next_move = new_board.choose_move()
        return move_list

class SolitaireMancalaBad:
    def __init__(self):
        self._board = [0]

    def set_board(self, configuration):
        self._board = configuration[:]

    def __str__(self):
        return str([self._board[i] for i in range((len(self._board) - 1), (-1), (-1))])

    def get_num_seeds(self, house_num):
        return self._board[house_num]

    def is_legal_move(self, house_num):
        if ((house_num == 0) or (house_num >= len(self._board))):
            return False
        else:
            return (house_num == self._board[house_num])

    def apply_move(self, house_num):
        if self.is_legal_move(house_num):
            for i in range(house_num):
                self._board[i] += 1
            self._board[house_num] = 0

    def choose_move(self):
        for i in self._board[1:]:
            if self.is_legal_move(i):
                return i
        return 0

    def is_game_won(self):
        won = True
        for i in self._board[1:]:
            if (i != 0):
                won = False
        return won

    def plan_moves(self):
        moves = []
        while True:
            move = self.choose_move()
            if ((move == 0) or self.is_game_won()):
                break
            else:
                self.apply_move(move)
                moves.append(move)
        return moves


# %%
from utils import gen_all_sequences

choices = set(range(11))

c_game = SolitaireMancala()
b_game = SolitaireMancalaBad()

for seq in gen_all_sequences(choices, 3):
    config = [0] + list(seq)

    c_game.set_board(config)
    b_game.set_board(config)

    c_game_moves = c_game.plan_moves()
    b_game_moves = b_game.plan_moves()

    if c_game_moves != b_game_moves:
        print config, c_game_moves, b_game_moves


# %%
d = {
    "Cursor": [15.0, 0.1],
    "Grandma": [100.0, 0.5],
    "Farm": [500.0, 4.0],
    "Factory": [3000.0, 10.0],
    "Mine": [10000.0, 40.0],
    "Shipment": [40000.0, 100.0],
    "Alchemy Lab": [200000.0, 400.0],
    "Portal": [1666666.0, 6666.0],
    "Time Machine": [123456789.0, 98765.0],
    "Antimatter Condenser": [3999999999.0, 999999.0]
}

import math
from pprint import pprint

t0 = 0
cps = 1.
total_cc = 0.
net_cc = 0.
T = 10000000000
GROWTH_C = 0.15
DISCOUNT_RATE = 1E-6
built = {k:0 for k in d}

def present_value(pmt, rate, npmt, n2pmt):
    annu = (1 + (1 + rate) ** (-npmt)) / rate
    pval = annu * ((1 + rate) ** (-n2pmt)) * pmt
    return pval
    
def choose_move():
    max_k, max_pv, jump = None, float('-inf'), float('-inf')
    rT = T - t0
    r = max(1/rT, DISCOUNT_RATE)
    for k, v in d.items():
        t_needed = math.ceil(max(v[0] - net_cc, 0) / cps)
        pv = present_value(v[1], DISCOUNT_RATE, rT - t_needed, t_needed)
    
        if max_k is None or pv > max_pv:
            max_k, max_pv = k, pv
            jump = t_needed
    
    return max_k, jump

def perform_move(k):
    global cps, net_cc

    built[k] += 1
    net_cc -= d[k][0]
    cps += d[k][1]
    d[k][0] *= 1 + GROWTH_C

def tick(jump=1):
    # allows for 0 jump, for multiple choices
    global t0, total_cc, net_cc
    actual_jump = min(jump, T-t0)
    t0 += actual_jump
    total_cc += cps * actual_jump
    net_cc += cps * actual_jump

def simulation():
    global t0, T
    while t0 < T:
        move, jump = choose_move()
        tick(jump)
        if move is not None:
            perform_move(move)
    
%time simulation()
print 'Total CC = {:.3}'.format(total_cc)
print 'Has CC = {:.2}'.format(net_cc)
print 'Spent = {:.2}'.format(total_cc - net_cc)
print 'CPS = {:.2}'.format(cps)
pprint(built)
pprint(d)


# %%
from poc_clicker_provided import BuildInfo

a = BuildInfo()
print a.get_cost('Farm')
a. update_item('Farm')
print a.get_cost('Farm')



# %%
def genfunc(endfunc):
    num = 0
    while True:
        if endfunc(num):
            break
        yield num
        num += 1

def endfn(num):
    if num == 7:
        return True
    return False

for g in genfunc(endfn):
    print g
# %%
