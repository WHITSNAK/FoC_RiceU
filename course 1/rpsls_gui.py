# GUI-based version of RPSLS

###################################################
# Student should add code where relevant to the following.

import simplegui
from random import randrange

# Functions that compute RPSLS
def name_to_number(name):
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        return


def number_to_name(number):
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        return

def is_win(a, b):
    c = (a - b) % 5
    
    if c in [1, 2]:
        return 1
    elif c in [3, 4]:
        return -1
    else:
        return 0

def rpsls(choice):
    player_n = name_to_number(choice)
    if player_n is None:
        print 'Error: Bad input "{}" to rpsls\n'.format(choice)
        return
    
    computer_n = randrange(0, 5)
    
    print('Player chooses {}'.format(number_to_name(player_n)))
    print('Computer chooses {}'.format(number_to_name(computer_n)))
    
    win_code = is_win(player_n, computer_n)
    if win_code == 1:
        print('Player wins!\n')
    elif win_code == -1:
        print('Computer wins!\n')
    else:
        print('Player and computer tie!\n')
     
    
# Handler for input field
def get_guess(guess):
    rpsls(guess)


# Create frame and assign callbacks to event handlers
frame = simplegui.create_frame("GUI-based RPSLS", 200, 200)
frame.add_input("Enter guess for RPSLS", get_guess, 200)


# Start the frame animation
frame.start()


###################################################
# Test

get_guess("Spock")
get_guess("dynamite")
get_guess("paper")
get_guess("lazer")

###################################################
# Sample expected output from test
# Note that computer's choices may vary from this sample.

#Player chose Spock
#Computer chose paper
#Computer wins!
#
#Error: Bad input "dynamite" to rpsls
#
#Player chose paper
#Computer chose scissors
#Computer wins!
#
#Error: Bad input "lazer" to rpsls
#
