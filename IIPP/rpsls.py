# Rock-paper-scissors-lizard-Spock
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

from random import randrange


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
                 
    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
