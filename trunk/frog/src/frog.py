'''frog.py

Our hero!
'''
import os
from pyglet import image
from pyglet import media
from pyglet.window import key

import util

DIR = os.path.dirname(__file__)

# we load some nice looking images for the frog as a playing character.
# the first one is that of a frog at rest
img_filename = os.path.join(DIR, "images", 'frogng1.png')
frog_facing_right = image.load(img_filename)
# the second is that of a moving frog; see next comment
img_filename = os.path.join(DIR, "images", 'frogng2.png')
frog_moving_right = image.load(img_filename)
# Using these two images creates a problem (later on) as they do not have
# the same width: the image of the moving frog, with its leg extended,
# is wider than that of the frog at rest. When blitting an image, we
# normally specify the position by the bottom left corner; however, to
# keep the image from "wobbling", we need to blit it so that the center (axis)
# of the two images (at rest, and moving) coincide.

# image used to display remaining lives
img_filename = os.path.join(DIR, "images", 'frog.png')
big_frog = image.load(img_filename)


img_filename = os.path.join(DIR, "images", 'croak1.png')
frog_dying1 = image.load(img_filename)
img_filename = os.path.join(DIR, "images", 'croak2.png')
frog_dying2 = image.load(img_filename)
img_filename = os.path.join(DIR, "images", 'croak3.png')
frog_dying3 = image.load(img_filename)
img_filename = os.path.join(DIR, "images", 'croak4.png')
frog_dying4 = image.load(img_filename)

img_filename = os.path.join(DIR, "images", 'sploosh1.png')
frog_sinking4 = image.load(img_filename)
img_filename = os.path.join(DIR, "images", 'sploosh2.png')
frog_sinking3 = image.load(img_filename)
img_filename = os.path.join(DIR, "images", 'sploosh3.png')
frog_sinking2 = image.load(img_filename)
img_filename = os.path.join(DIR, "images", 'sploosh4.png')
frog_sinking1 = image.load(img_filename)

#http://www.sound-effect.com/pirsounds/WEB_DESIGN_SOUNDS_WAV1/SOUNDFX/SPLASH.WAV
snd_filename = os.path.join(DIR, "sounds", 'splash.wav')
splash_sound = media.load(snd_filename, streaming=False)
#http://www.sound-effect.com/pirsounds/WEB_DESIGN_SOUNDS_WAV1/SOUNDFX/METALBAN.WAV
snd_filename = os.path.join(DIR, "sounds", 'metal_bang.wav')
metal_bang_sound = media.load(snd_filename, streaming=False)
#http://osabisi.sakura.ne.jp/m2/mtc/se/saku02_r.wav
snd_filename = os.path.join(DIR, "sounds", 'splat.wav')
crush_sound = media.load(snd_filename, streaming=False)
#http://www.vionline.com/snd/cuckoo.wav
snd_filename = os.path.join(DIR, "sounds", 'cuckoo.wav')
out_of_time_sound = media.load(snd_filename, streaming=False)
#http://www.vionline.com/snd/drums1.wav
#snd_filename = os.path.join(DIR, "sounds", 'drums1.wav')
#safe_landing_sound = media.load(snd_filename, streaming=False)
#http://www.greatwebdesign.biz/little-league/sounds/crowd.wav
snd_filename = os.path.join(DIR, "sounds", 'crowd.wav')
safe_landing_sound = media.load(snd_filename, streaming=False)
#http://www.vionline.com/snd/chimeup.wav
level_completed_sound_fname = os.path.join(DIR, "sounds", 'chimeup.wav')

def level_completed_play():
    '''for some reason, using streaming leads to a "broken up" sound for the
    following sound.
    '''
    media.load(level_completed_sound_fname).play()

class Frog(key.KeyStateHandler):
    '''Our hero
    '''
    def __init__(self, game, world):
        super(Frog, self).__init__()
        self.world = world
        self.game = game
        self.at_rest_image = frog_facing_right
        self.moving_image = frog_moving_right
        self.rotation = 90  # starting pointing up
        # since we are starting 90 degree rotated, width and height are inverted
        self.width = self.at_rest_image.height
        self.height = self.at_rest_image.width
        # when a frog is moving, an animation is started with a given
        # positive time duration.  Initially, we set to negative value
        # as no animation is taking place
        self.animation_time = -1
        self.min_y = 10
        #self.spare_lives is set from Game()
        self.dying = False
        self.sinking = False
        # invincible state can be toggled within game by pressing
        # ctrl-shift-I
        self.invincible = False
        self.new_frog(new_life=False)

    def new_frog(self, new_life=True, out_of_time=False):
        self.lane = 0
        if new_life:
            self.spare_lives -= 1
            self.dying = 1.01  # time for animation
            if self.spare_lives < 0:
                self.game.over = True
            elif out_of_time:
                self.game.out_of_time = True
            else:
                self.game.time_remaining.restart()
        else:
            self.x = (self.world.width - self.width)/2
            self.y = self.min_y

    def start_new_level(self, lives):
        self.spare_lives = lives

    def jump(self, dx=0, dy=0):
        '''frog changes position either horizontally or vertically'''
        # horizontal motion: half a lane distance, for finer control
        if dx != 0:
            self.x += dx*self.world.lane_width/2
            return
        # For vertical motion, we need to keep track of the lane changes
        self.y += dy*self.world.lane_width
        if dy < 0:
            self.lane -= 1
        else:
            self.lane += 1
        # prevent going down below starting point
        if self.y < self.min_y:
            self.y = self.min_y
            self.lane = 0

    def check_position(self, dt, pads, cars, logs):
        '''check to see if we reached a "winning" position or if the
           frog has died'''

        if self.lane == self.world.pad_lane:
            pad = util.detect_collision(self, pads, self.width)
            if pad:
                if pad.occupied:
                    if not self.game.level_completed and not self.invincible:
                        metal_bang_sound.play()
                        self.new_frog()
                    else:
                        return
                else:
                    pad.set_occupied()
                    self.game.score.reached_pad()
                    # determine if level has been completed
                    completed_level = True
                    for pad in pads:
                        if not pad.occupied:
                            completed_level = False
                            break
                    if completed_level:
                        level_completed_play()
                        self.game.set_level_completed(self.spare_lives)
                        self.new_frog(new_life=False)
                    else:
                        safe_landing_sound.play()
                        self.new_frog(new_life=False)
            elif not self.invincible:
                self.sinking = True
                splash_sound.play()
                self.new_frog()
        elif self.lane in self.world.lane_with_logs and not self.invincible:
            log = util.detect_collision(self, logs, 5)
            if not log or log.sunk:
                self.sinking = True
                splash_sound.play()
                self.new_frog()
            else:
                self.x += log.vx*dt
        elif util.outside_world(self, self.world) and not self.invincible:
            crush_sound.play()
            self.new_frog()
        else:
            car = util.detect_collision(self, cars, 2)
            if car and not self.invincible:
                crush_sound.play()
                self.new_frog()

    def update(self, dt, pads, cars, logs):
        '''simplest case is just drawing == blitting; animation will follow'''
        self.display_lives()
        if self.game.paused:
            return
        if not self.dying:
            if self[key.LEFT]:
                self.rotation = 180
                self.start_moving()
                self.jump(dx=-1)
                self[key.LEFT] = False
            elif self[key.RIGHT]:
                self.rotation = 0
                self.start_moving()
                self.jump(dx=1)
                self[key.RIGHT] = False
            elif self[key.UP]:
                self.rotation = 90
                self.start_moving()
                self.jump(dy=1)
                self[key.UP] = False
            elif self[key.DOWN]:
                self.rotation = -90
                self.start_moving()
                self.jump(dy=-1)
                self[key.DOWN] = False

            self.check_position(dt, pads, cars, logs)
            if self.game.time_remaining.time_left < 0:
                out_of_time_sound.play()
                self.new_frog(out_of_time=True)
            if self.spare_lives > -1:
                previous = self.animation_time
                self.animation_time -= dt
                # adjust parameters so as to deal only with
                # at rest image (not the moving one)
                if self.rotation in [0, 180]:
                    self.width = self.at_rest_image.width
                    self.height = self.at_rest_image.height
                else:
                    self.width = self.at_rest_image.height
                    self.height = self.at_rest_image.width
                if self.animation_time < 0: # no longer moving
                    util.draw_rotated(self, self.at_rest_image)
                else:
                    # draw from previous position, with moving image
                    saved_x, saved_y = self.x, self.y
                    self.x, self.y = self.old_x, self.old_y
                    util.draw_rotated(self, self.moving_image)
                    self.x, self.y = saved_x, saved_y
        else:
            self.die(dt)

    def start_moving(self):
        previous = self.animation_time
        # animation lasts barely long enough to see it; since we determine
        # the end of animation by crossing 0, add a tiny offset
        # to avoid accidental strict equality to zero.
        self.animation_time = 1.0/20 + 0.000001
        self.old_x = self.x
        self.old_y = self.y

    def die(self, dt):
        self.dying -= dt
        if self.dying > 0.75:
            if self.sinking:
                frog_sinking1.blit(self.x, self.y)
            else:
                frog_dying1.blit(self.x, self.y)
        elif self.dying > 0.5:
            if self.sinking:
                frog_sinking2.blit(self.x, self.y)
            else:
                frog_dying2.blit(self.x, self.y)
        elif self.dying > 0.25:
            if self.sinking:
                frog_sinking3.blit(self.x, self.y)
            else:
                frog_dying3.blit(self.x, self.y)
        elif self.dying > 0:
            if self.sinking:
                frog_sinking4.blit(self.x, self.y)
            else:
                frog_dying4.blit(self.x, self.y)
        else:
            self.dying = False
            self.sinking = False
            self.game.paused = True
            self.x = (self.world.width - self.at_rest_image.width)/2
            self.y = self.min_y

    def display_lives(self):
        n = self.spare_lives
        x = self.world.width
        y = self.world.height + self.min_y
        while n > 0:
            x -= (big_frog.width + 10)
            big_frog.blit(x, y)
            n -= 1