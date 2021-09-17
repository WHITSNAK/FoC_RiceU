try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
from random import randrange

range_state = 0
true_num = None
max_chances = None

# helper function to start and restart the game
def new_game():
    global true_num, max_chances
    
    if range_state == 0:
        l, r = 0, 100
    elif range_state == 1:
        l, r = 0, 1000
    else:
        raise ValueError('Bad range_state')
        
    max_chances = math.ceil(math.log(r-l+1)/math.log(2))
    true_num = randrange(l, r)
    
    print('New game. Range is [{}, {})'.format(l, r))
    print('Number of remaining guesses is {}\n'.format(max_chances))


# define event handlers for control panel
def range100():
    global range_state
    
    range_state = 0
    new_game()

def range1000():
    global range_state
    
    range_state = 1
    new_game()
    
def input_guess(guess):
    global max_chances
    
    gnum = int(guess)
    max_chances -= 1
    print('Guess was {}'.format(gnum))
    print('Number of remaining guesses is {}'.format(max_chances))
    
    if true_num == gnum:
        print('Correct!\n')
        new_game()
        return
    
    if max_chances == 0:
        print('You ran out of guessess. The number was {}\n'.format(true_num))
        new_game()
        return
        
    if true_num > gnum:
        print('Higher!\n')
    else:
        print('Lower!\n')

        
        
frame = simplegui.create_frame('Guess the number', 200, 200)
frame.add_button('New game', new_game, 100)
frame.add_button('Range to 100', range100, 100)
frame.add_button('Range to 1000', range1000, 100)
frame.add_input('Enter guess', input_guess, 100)
frame.start()

new_game()

