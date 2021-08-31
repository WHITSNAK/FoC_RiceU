# Basic infrastructure for Bubble Shooter

import simplegui
import random
import math

# Global constants
WIDTH = 800
HEIGHT = 600
FIRING_POSITION = [WIDTH // 2, HEIGHT]
FIRING_LINE_LENGTH = 60
FIRING_ANGLE_VEL_INC = 0.02
BUBBLE_RADIUS = 20
COLOR_LIST = ["Red", "Green", "Blue", "White"]

# global variables
firing_angle = math.pi*0.25
firing_angle_vel = 0
bubble_stuck = True

# firing sound
firing_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/Collision8-Bit.ogg")


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)


# class defintion for Bubbles
class Bubble:
    
    def __init__(self, sound=None):
        self.pos = list(FIRING_POSITION)
        self.vel = [0, 0]
        self.color = random.choice(COLOR_LIST)
        self.sound = sound
    
    def update(self):
        if self.pos[0]-BUBBLE_RADIUS<0 or self.pos[0]+BUBBLE_RADIUS>WIDTH:
            self.vel[0] *= -1
            
        self.pos[0] += self.vel[0]
        self.pos[1] -= self.vel[1]
        
    def fire_bubble(self, vel):
        self.vel = vel
        if self.sound:
            self.sound.rewind()
            self.sound.play()
        
    def is_stuck(self): 
        pass

    def collide(self, bubble):
        pass
            
    def draw(self, canvas):
        canvas.draw_circle(self.pos, BUBBLE_RADIUS, 1, 'White', self.color)

        
# define keyhandlers to control firing_angle
def keydown(key):
    global a_bubble, firing_angle, firing_angle_vel, bubble_stuck
    
    if key == simplegui.KEY_MAP['left']:
        firing_angle_vel = FIRING_ANGLE_VEL_INC
    elif key == simplegui.KEY_MAP['right']:
        firing_angle_vel = - FIRING_ANGLE_VEL_INC
    elif key == simplegui.KEY_MAP['space']:
        angle = angle_to_vector(firing_angle)
        a_bubble.fire_bubble([angle[0]*4, angle[1]*4])

def keyup(key):
    global firing_angle_vel
    
    firing_angle_vel = 0
    
# define draw handler
def draw(canvas):
    global firing_angle, a_bubble, bubble_stuck
    
    # update firing angle
    firing_angle += firing_angle_vel
    
    # draw firing line
    angle = angle_to_vector(firing_angle)
    bottom_pos = FIRING_POSITION
    head_pos = (
        bottom_pos[0] + angle[0]*FIRING_LINE_LENGTH,
        bottom_pos[1] - angle[1]*FIRING_LINE_LENGTH  # reverse y
    )
    canvas.draw_line(bottom_pos, head_pos, 10, 'White')
    
    # update a_bubble and check for sticking
    a_bubble.update()
    
    # draw a bubble and stuck bubbles
    a_bubble.draw(canvas)
    
 
# create frame and register handlers
frame = simplegui.create_frame("Bubble Shooter", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_draw_handler(draw)

# create initial buble and start frame
a_bubble = Bubble(sound=firing_sound)
frame.start()