# implementation of card game - Memory

import simplegui
import random

N = 16  # number of cards in the deck
FONT_SIZE = 60
WIDTH, HEIGHT = N*50, 100
DEBUG = True

# helper functions
def new_game():
    """Init a new game"""
    global deck, exposed, chosen, turns, truth
    
    # getting the random deck
    deck = list(range(int(N/2))) * 2
    random.shuffle(deck)
    
    # construct the truth dictionary for quick lookup
    n_to_pair = {}
    for i, n in enumerate(deck):
        if n not in n_to_pair:
            n_to_pair[n] = [i]
        else:
            n_to_pair[n].append(i)
    truth = {tuple(v):k for k,v in n_to_pair.items()}
    
    # other things to keep track of
    exposed = {i:False for i in range(len(deck))}
    chosen = []
    turns = 0
    
    update_label()
    
    if DEBUG:
        print 'Deck:', deck
        print 'Truth:', truth
    
    
def card_vertices(center):
    return (
        (center[0]-25, center[1]-50),
        (center[0]+25, center[1]-50),
        (center[0]+25, center[1]+50),
        (center[0]-25, center[1]+50),
    )

def num_centered_pos(pos):
    return (pos[0]-FONT_SIZE/4, pos[1]+FONT_SIZE/4)

def state():
    return len(chosen)

def clear_chosen(is_match):
    global exposed, chosen
    
    if not is_match:
        for c in chosen:
            exposed[c] = False
    chosen = []
    
def inc_turns():
    global turns
    turns += 1
    
def update_label():
    label.set_text('Turns = {}'.format(str(turns)))

def is_match():
    if len(chosen) != 2: return
    
    if tuple(sorted(chosen)) in truth:
        return True
    else:
        return False
                   
# define event handlers
def mouseclick(pos):
    global chosen
    
    i = pos[0]//50
    
    # ignore clicks on exposed card
    if exposed[i]: return

    state_code = state()
    if state_code == 0:  # new start
        chosen.append(i)
        inc_turns()
        update_label()
    else:
        if state_code == 1:
            chosen.append(i)
        else:
            clear_chosen(is_match())
            chosen.append(i)
            inc_turns()
            update_label()
    
    exposed[i] = True
    
    if DEBUG:
        print 'State:', state_code, 'Chosen cards:', chosen
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(N):
        center = 25 + i*50, 50
        if exposed[i]:
            canvas.draw_polygon(
                card_vertices(center),
                1, 'Black', 'Black'
            )
            canvas.draw_text(
                str(deck[i]), num_centered_pos(center),
                FONT_SIZE, 'White'
            )
        else:
            canvas.draw_polygon(
                card_vertices(center),
                1, 'Black', 'Green'
            )


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label('Placeholder')

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
# Always remember to review the grading rubric