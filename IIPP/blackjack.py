# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "game outcome"
score = 0
debug = True

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            raise ValueError('Invalid card suit or rank')

    def __str__(self):
        return self.suit + self.rank
    
    def __repr__(self):
        return self.__str__()

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, front=True):
        """
        pos: top left corner of the card XY coordinates
        """
        canvas_p = [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]]
        if front:
            card_loc = (
                CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit)
            )
            canvas.draw_image(card_images, card_loc, CARD_SIZE, canvas_p, CARD_SIZE)
        else:
            back_loc = CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0], CARD_BACK_CENTER[1]
            canvas.draw_image(card_back, back_loc, CARD_BACK_SIZE, canvas_p, CARD_BACK_SIZE)
        
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        card_str = ' '.join([c.__str__() for c in self.cards])
        return 'Hand contains %s' % card_str
    
    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        v = 0
        has_ace = False
        for c in self.cards:
            rank = c.get_rank()
            v += VALUES[rank]
            
            if rank == 'A':
                has_ace = True
        
        if has_ace and v+10 <= 21:
            return v + 10
        return v
    
    def is_busted(self):
        return self.get_value() > 21
   
    def draw(self, canvas, pos, has_hole=False):
        for i, c in enumerate(self.cards):
            _pos = pos[0] + i*(15+CARD_SIZE[0]), pos[1]
            c.draw(canvas, _pos, front=not(has_hole and i == 0))
 
        
# define deck class 
class Deck:
    def __init__(self):
        cards = []
        for suit in SUITS:
            for rank in RANKS:
                cards.append(Card(suit, rank))
                
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        s = ' '.join([c.__str__() for c in self.cards])
        return 'Deck contains %s' % s


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer_hand, player_hand, score
    
    # folder/surrender
    if in_play:
        outcome = 'Folded, another deal?'
        score -= 1
        in_play = False
        return
    
    in_play = True
    outcome = 'Hit or Stand?'
    deck = Deck()
    dealer_hand = Hand()
    player_hand = Hand()
    
    deck.shuffle()
    for _ in range(2): # 2 cards each hand
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
    
    if debug:
        print '\nNew deal,', 'current score = {}'.format(score)
        print 'Dealer', dealer_hand, '=', dealer_hand.get_value()
        print 'Player', player_hand, '=', player_hand.get_value()
        

def hit():
    global in_play, score, outcome
    
    if not in_play: return

    player_hand.add_card(deck.deal_card())
    
    if debug:
        print 'Hit!'
        print 'Player', player_hand, '=', player_hand.get_value()
    
    if player_hand.is_busted():
        outcome = 'You have busted, new deal?'
        in_play = False
        score -= 1

        
def stand():
    global in_play, score, outcome
    
    if not in_play: return
    
    if debug:
        print 'Dealer is drawing cards'
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
    
    pv, dv = player_hand.get_value(), dealer_hand.get_value()
    if dv > 21:
        score += 1
        outcome = 'Dealer is busted, you win! New deal?'
        
        if debug:
            print 'Dealer =', dealer_hand, dv
            print 'Dealer =', dv, 'Player =', pv
    else:
        if pv > dv:
            score += 1
            outcome = 'Your value is higher, you win! New deal?'
        else:
            score -= 1
            outcome = 'Dealer value is higher, you loss! New deal?'
        
        if debug:
            print 'Dealer', dealer_hand, '=', dealer_hand.get_value()
            print 'Player', player_hand, '=', player_hand.get_value()
    
    in_play = False
   

# draw handler    
def draw(canvas):
    canvas.draw_text('Blackjack', (CARD_SIZE[0]/2,50), 35, 'White')
    canvas.draw_text(outcome, (CARD_SIZE[0]/2,275+CARD_SIZE[1]/2), 25, 'White')
    canvas.draw_text('Score = {}'.format(score), (CARD_SIZE[0]*6,50), 25, 'White')
    
    dealer_hand.draw(canvas, (CARD_SIZE[0]/2, 150), has_hole=in_play)
    player_hand.draw(canvas, (CARD_SIZE[0]/2, 400))


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

# remember to review the gradic rubric