"""
Rice rock verison of spaceship Astriod aracde game 
"""

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
from random import random, choice

# globals for user interface
WIDTH = 800
HEIGHT = 600
CANVAS_SIZE = (WIDTH, HEIGHT)
CANVAS_CENTER = (CANVAS_SIZE[0]/2, CANVAS_SIZE[1]/2)

started = False
score = 0
lives = 3
time = 0
game_time = 0

MAX_ROCKS = 12
ROCK_SPAWN_INTERVAL = 1000.0  #ms
SAFE_ZONE_C = 8
rock_timer = None
rocks = set()

my_ship = None
ship_initial_pos = list(CANVAS_CENTER)
missiles = set()

class ImageInfo:
    def __init__(self, size, center=None, radius=0, lifespan=None, animated=False):
        self.size = size
        self.center = [self.size[0]/2, self.size[1]/2] if not center else center
        self.radius = radius
        self.lifespan = lifespan if lifespan else float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([90, 90], radius=35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([10, 10], radius=3, lifespan=50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([90, 90], radius=40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([128, 128], radius=17, lifespan=24, animated=True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack1 = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
soundtrack2 = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# utility functions
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    return math.sqrt((p[0]-q[0])**2 + (p[1]-q[1])**2)


def screen_wrap(pos):
    """Wraps around the screen if needed given a postiion"""
    return [pos[0] % WIDTH, pos[1] % HEIGHT]


class Ship:
    TURN_SPEED = (3/2)*math.pi/60  # 75% of circle per 60 FPS
    FRICTION_LAM = 1-(1/45.)  # stop in 45 FPS
    TRUST_SPEED = 6 * (1-FRICTION_LAM)  # max 6 px/FPS speed
    MISSILE_SPEED = 7
    
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        img_center = list(self.image_center)
        if self.thrust:
            img_center[0] += self.image_size[0]  # moves to thrust one
            
        canvas.draw_image(
            self.image, img_center, self.image_size,
            self.pos, self.image_size, self.angle
        )

    def update(self):
        # position update
        new_pos = [self.pos[0] + self.vel[0], self.pos[1] - self.vel[1]]
        self.pos = screen_wrap(new_pos)
        
        # orientation update
        self.angle += self.angle_vel
        
        # velocity & friction update
        self.vel[0] = self.FRICTION_LAM * self.vel[0]
        self.vel[1] = self.FRICTION_LAM * self.vel[1]
        
        # acceleration update
        if self.thrust:
            dir_v = angle_to_vector(self.angle)
            self.vel[0] += dir_v[0] * self.TRUST_SPEED
            self.vel[1] += -dir_v[1] * self.TRUST_SPEED
        
    def turn(self, direction):
        if direction == 'left':
            self.angle_vel = -self.TURN_SPEED
        elif direction == 'right':
            self.angle_vel = self.TURN_SPEED
        elif direction == 'hold':
            self.angle_vel = 0 
    
    def engine(self, state):
        if state == 'on':
            self.thrust = True
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        elif state == 'off':
            self.thrust = False
            ship_thrust_sound.pause()
            
    def shoot(self):
        ship_dir = angle_to_vector(self.angle)
        p = [ship_dir[i] * self.radius + p for i, p in enumerate(self.pos)]
        v = [self.vel[0] + ship_dir[0] * self.MISSILE_SPEED,
             self.vel[1] - ship_dir[1] * self.MISSILE_SPEED]
        
        missile = Sprite(p, v, 0, 0, missile_image, missile_info, missile_sound)
        missiles.add(missile)
            
            
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        
        # play it when its created
        if sound:
            sound.rewind()
            sound.play()
            
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        canvas.draw_image(
            self.image, self.image_center, self.image_size,
            self.pos, self.image_size, self.angle
        )
    
    def update(self):
        """Update motion
        return -> boolean flag on whether passes the lifespan
        """
        # position update
        new_pos = [self.pos[0] + self.vel[0], self.pos[1] - self.vel[1]]
        self.pos = screen_wrap(new_pos)
        
        # orientation update
        self.angle += self.angle_vel
        
        # handle lifespan
        self.age += 1
        flag = False
        if self.age >= self.lifespan:
            flag = True
        return flag
    
    def collide(self, other):
        d = dist(self.pos, other.get_pos())
        total_r = self.radius + other.get_radius()
        return d <= total_r
    

# Event handlers
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.turn(direction='left')
    elif key == simplegui.KEY_MAP['right']:
        my_ship.turn(direction='right')
    elif key == simplegui.KEY_MAP['up']:
        my_ship.engine(state='on')
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()


def keyup(key):
    if key in [simplegui.KEY_MAP['left'], simplegui.KEY_MAP['right']]:
        my_ship.turn(direction='hold')
    elif key == simplegui.KEY_MAP['up']:
        my_ship.engine(state='off')


def mouseclick(pos):
    global started
    if not started:
        started = True
        start_game()


def draw(canvas):
    """Main game drawing function"""
    global time, game_time, lives, score, started
    
    time += 1  # 1 per frame ticks

    # animiated background
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(),
                      nebula_info.get_size(),
                      [WIDTH/2, HEIGHT/2], CANVAS_SIZE)
    canvas.draw_image(debris_image, center, size,
                      (wtime - WIDTH/2, HEIGHT/2), CANVAS_SIZE)
    canvas.draw_image(debris_image, center, size,
                      (wtime + WIDTH/2, HEIGHT/2), CANVAS_SIZE)
    
    # draw lives and score
    lives_pos = [WIDTH*0.05, HEIGHT*0.08]
    score_pos = [WIDTH*0.85, lives_pos[1]]
    draw_stats(canvas, 'Lives', lives, lives_pos)
    draw_stats(canvas, 'Scores', score, score_pos)
    
    # draw and update ship
    my_ship.draw(canvas)
    my_ship.update()
    
    # draw new game welcome screen
    if not started:
        canvas.draw_image(
            splash_image,
            splash_info.get_center(), splash_info.get_size(),
            CANVAS_CENTER, splash_info.get_size()
        )
        return  # no sprites while in welcome screen
    
    # in the game!
    game_time += 1
    
    # draw and updates sprites
    process_sprite_group(rocks, canvas)
    process_sprite_group(missiles, canvas)
    
    # check collision rocks vs ship
    col_set = collide_g2o(rocks, my_ship)
    if len(col_set) > 0:
        lives -= 1
        rocks.difference_update(col_set)
        if lives <= 0:
            new_game()
    
    # colision rocks vs missiles
    rock_set, missile_set = collide_g2g(rocks, missiles)
    if len(rock_set) > 0 or len(missile_set) > 0:
        score += len(missile_set)
        rocks.difference_update(rock_set)
        missiles.difference_update(missile_set)
    

# game helper functions
def draw_stats(canvas, title, num, pos, font_size=23, color='White'):
    """Draw helper functions for game statistics [lives, scores]"""
    num_pos = [pos[0], pos[1]+font_size]
    canvas.draw_text(title, pos, font_size, color)
    canvas.draw_text(str(num), num_pos, font_size, color)
            

def process_sprite_group(group, canvas):
    """Utility helper to draw and update motions of all items in a group
    Also checks whether a sprite is about to die out
    """
    remove = set()
    for g in group:
        g.draw(canvas)
        death_flag = g.update()
        if death_flag: remove.add(g)
    group.difference_update(remove)
        
        
def collide_g2o(group, other):
    """Test a group of objects whether is collided with an item
    return:
        Yes: remove collided objects -> True
        No: do nothing -> False
    """
    remove = set([])
    for g in group:
        if g.collide(other):
            remove.add(g)
    return remove


def collide_g2g(group_a, group_b):
    """Test collision between two groups
    return: collided set for each group a and b
    """
    a_remove, b_remove = set(), set()
    for a in group_a:
        rset = collide_g2o(group_b, a)
        if len(rset) > 0:
            a_remove.add(a)
            b_remove.update(rset)
    return a_remove, b_remove


def random_pos():
    return [random()*WIDTH, random()*HEIGHT]


def random_vel(mag):
    d = 1, -1
    return [random()*choice(d)*mag, random()*choice(d)*mag]


def rock_spawner():
    """Spawns a rock"""
    global rocks
    
    # random pos, vel, and angular_v
    dirs = [1, -1]
    
    # anywhere in the canvas, not too close to the ship
    p = random_pos()
    while dist(p, my_ship.get_pos()) <= my_ship.get_radius()*SAFE_ZONE_C:
        p = random_pos()
    
    # speed U(0,2) px per frame + incr by the time
    rock_speed_c = game_time/1800. + 2
    v = random_vel(mag=rock_speed_c)
    av = random()*choice(dirs)/15.  # acce U(0,5) per second

    rock = Sprite(p, v, 0, av, asteroid_image, asteroid_info)
    
    if len(rocks) < MAX_ROCKS:
        rocks.add(rock)
        
    
def new_game():
    global started, lives, score, game_time
    global rock_timer, my_ship, rocks, missiles
    
    started = False
    lives = 3
    score = 0
    game_time = 0
    
    if rock_timer: rock_timer.stop()
    rock_timer = simplegui.create_timer(ROCK_SPAWN_INTERVAL, rock_spawner)
    rocks = set()
        
    my_ship = Ship(ship_initial_pos, [0,0], 0, ship_image, ship_info)
    missiles = set()
    
    # background music
    soundtrack2.pause()
    soundtrack1.rewind()
    soundtrack1.play()
    
    
def start_game():
    global started
    
    started = True
    rock_timer.start()
    
    # background music
    soundtrack1.pause()
    soundtrack2.rewind()
    soundtrack2.play()
    

    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouseclick)
frame.add_button('Reset', new_game, 100)
frame.add_button('Start', start_game, 100)

# starting up the game
frame.start()
new_game()

