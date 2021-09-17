"""
Implementation of classic arcade game Pong
"""

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
BALL_LINE = 1
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
PAD_V = 4
LEFT = -1
RIGHT = 1


def inc_score(cc):
    global score1, score2
    
    if cc == 'L':
        score2 += 1
    elif cc == 'R':
        score1 += 1
  

def inc_speed(pct):
    global ball_vel
    
    ball_vel[0] *= 1 + pct
    ball_vel[1] *= 1 + pct


def check_collide(pos):
    """
    Check the ball position in relation to 4 sides
    gutter width is taken in account
    """
    x, y = ball_pos[0], ball_pos[1]
    actual_r = BALL_RADIUS + BALL_LINE/2
    
    if x <= actual_r + PAD_WIDTH:
        return 'L'
    elif x >= WIDTH - PAD_WIDTH - actual_r:
        return 'R'
    elif y <= actual_r:
        return 'U'
    elif y >= HEIGHT - actual_r:
        return 'D'
    else:
        return None

def update_ball():
    """Central update for ball"""
    global ball_pos, ball_vel
    
    collide_code = check_collide(ball_pos)
    
    # reflection
    if collide_code in ('L', 'R'):
        ball_vel[0] = ball_vel[0] * -1
    elif collide_code in ('U', 'D'):
        ball_vel[1] = ball_vel[1] * -1
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    return collide_code
    
 
def get_paddle_ps(pos):
    """Given the center coordinates, returns 4 vertexs"""
    return [
        (pos[0]-HALF_PAD_WIDTH, pos[1]+HALF_PAD_HEIGHT),
        (pos[0]+HALF_PAD_WIDTH, pos[1]+HALF_PAD_HEIGHT),
        (pos[0]+HALF_PAD_WIDTH, pos[1]-HALF_PAD_HEIGHT),
        (pos[0]-HALF_PAD_WIDTH, pos[1]-HALF_PAD_HEIGHT),
    ]

def update_paddle_pos(p, v):
    pos_y = p[1] + v[1]
    
    # check on top and botton margin
    if pos_y > HALF_PAD_HEIGHT-1 and pos_y < HEIGHT-HALF_PAD_HEIGHT+1:
        p[1] = pos_y
    return p


def has_paddle(cc):
    global paddle1_pos, paddle2_pos

    flag = False
    bpos = ball_pos[1]
    if cc == 'L':
        ppos = paddle1_pos
    elif cc == 'R':
        ppos = paddle2_pos
    else:
        return flag
    
    if bpos <= ppos[1] + HALF_PAD_HEIGHT and bpos >= ppos[1] - HALF_PAD_HEIGHT:
        flag = True
    return flag

 
    
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [
        direction * random.randrange(120, 240)/60.,
        -random.randrange(60, 180)/60.
    ]


def random_spawn():
    if random.random() < 0.5:
        direction = LEFT
    else:
        direction = RIGHT
    spawn_ball(direction)


# define event handlers
def new_game():
    """Init all location of velocities"""
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    score1, score2 = 0, 0
    paddle1_pos, paddle1_vel = [HALF_PAD_WIDTH, HEIGHT/2], [0, 0]
    paddle2_pos, paddle2_vel = [WIDTH-HALF_PAD_WIDTH, HEIGHT/2], [0, 0]
    
    random_spawn()
    

def draw(canvas):
    global score1, score2, ball_pos, ball_vel
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    collide_code = update_ball()
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, BALL_LINE, 'White', 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    update_paddle_pos(paddle1_pos, paddle1_vel)
    update_paddle_pos(paddle2_pos, paddle2_vel)
    
    # draw paddles
    canvas.draw_polygon(get_paddle_ps(paddle1_pos), 1, 'White', 'White')
    canvas.draw_polygon(get_paddle_ps(paddle2_pos), 1, 'White', 'White')
    
    # determine whether paddle and ball collide & scoring
    if collide_code in ('L','R'):
        if not has_paddle(collide_code):
            inc_score(collide_code)
            
            if collide_code == 'L':
                spawn_ball(RIGHT)
            else:
                spawn_ball(LEFT)
        else:
            inc_speed(0.1)
    
    # draw scores
    canvas.draw_text(str(score1), (200,100), 40, 'White')
    canvas.draw_text(str(score2), (400-30,100), 40, 'White')
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel[1] = -PAD_V
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel[1] = PAD_V
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel[1] = -PAD_V
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel[1] = PAD_V
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key in (simplegui.KEY_MAP['w'], simplegui.KEY_MAP['s']):
        paddle1_vel[1] = 0
    elif key in (simplegui.KEY_MAP['up'], simplegui.KEY_MAP['down']):
        paddle2_vel[1] = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', new_game, 100)


# start frame
new_game()
frame.start()
