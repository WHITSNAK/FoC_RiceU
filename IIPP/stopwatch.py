"""
template for "Stopwatch: The Game"
"""

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# define global variables
total_ticks = 0
is_stopped = True
scores, hits = 0, 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def tick_format(t):
    m, s, ms = 0, 0, t

    if ms // 10:
        s = ms // 10
        ms -= s * 10

    if s // 60:
        m = s // 60
        s -= m * 60

    return '{}:{:02}.{}'.format(m, s, ms)


def score_txt():
    return '{}/{}'.format(scores, hits)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    global is_stopped
    
    if is_stopped:
        timer.start()
        is_stopped = False


def stop_timer():
    global scores, hits, is_stopped
    
    if is_stopped: return
    
    timer.stop()
    if total_ticks % 10 == 0:
        scores += 1
    hits += 1
    is_stopped = True
    
def reset_timer():
    global total_ticks, scores, hits
    total_ticks = 0
    scores = 0
    hits = 0


# define event handler for timer with 0.1 sec interval
def tick():
    global total_ticks
    total_ticks += 1

    
# define draw handler
def draw(canvas):
    s = tick_format(total_ticks)
    canvas.draw_text(s, (50,110), 45, 'White')
    canvas.draw_text(score_txt(), (165, 20), 24, 'Green')
    
    
# create frame
frame = simplegui.create_frame('Stopwatch', 200, 200)

frame.add_button('Start', start_timer, 100)
frame.add_button('Stop', stop_timer, 100)
frame.add_button('Reset', reset_timer, 100)

timer = simplegui.create_timer(100, tick)

# register event handlers
frame.set_draw_handler(draw)

# start frame
frame.start()

# Please remember to review the grading rubric

