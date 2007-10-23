'''frog.py

Our hero!
'''
import os
from pyglet import image
from pyglet import media
from pyglet.window import key

import util

DIR = os.path.dirname(__file__)

img_filename = os.path.join(DIR, "images", 'frogng1.png')
frog_facing_right = image.load(img_filename)

img_filename = os.path.join(DIR, "images", 'frogng2.png')
frog_moving_right = image.load(img_filename)

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
    '''Our hero'''
    def __init__(self, game, world):
        super(Frog, self).__init__()
        self.world = world
        self.game = game
        self.at_rest_image = frog_facing_right#self.images[self.orientation]
        self.moving_image = frog_moving_right
        self.rotation = 90  # starting pointing up
        self.animation_time = -1
        # since we are starting 90 degree rotated, width and height are inverted
        self.width = self.at_rest_image.height
        self.height = self.at_rest_image.width

        self.min_y = 10
        self.lives = 4
        self.dying = False
        self.sinking = False
        self.new_frog(new_life=False)

    def new_frog(self, new_life=True, out_of_time=False):
        self.lane = 0
        if new_life:
            self.lives -= 1
            self.dying = 1.01  # time for animation
            if self.lives < 0:
                self.game.over = True
            elif out_of_time:
                self.game.out_of_time = True
            else:
                self.game.time_remaining.restart()
        else:
            self.x = (self.world.width - self.width)/2
            self.y = self.min_y

    def start_new_level(self, lives):
        self.lives = lives

    def jump(self, dy):
        '''move vertically'''
        self.y += dy*self.world.lane_width
        if dy < 0:
            self.lane -= 1
        else:
            self.lane += 1
        # prevent going down below starting point
        if self.y < self.min_y:
            self.y = self.min_y
            self.lane = 0

    def step(self, dx):
        '''move horizontally'''
        self.x += dx*self.world.lane_width/2

    def check_position(self, dt, pads, cars, logs):
        '''check to see if we reached a "winning" position or if the
           frog has died'''

        if self.lane == self.world.pad_lane:
            pad = util.detect_safe_landing(self, pads)
            if pad:
                if pad.occupied:
                    if not self.game.level_completed:
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
                        self.game.set_level_completed(self.lives)
                        self.new_frog(new_life=False)
                    else:
                        safe_landing_sound.play()
                        self.new_frog(new_life=False)
            else:
                self.sinking = True
                splash_sound.play()
                self.new_frog()
        elif self.lane in self.world.lane_with_logs:
            log = util.detect_collision(self, logs, 5)
            if not log:
                self.sinking = True
                splash_sound.play()
                self.new_frog()
            else:
                self.x += log.vx*dt
        elif util.outside_world(self, self.world):
            crush_sound.play()
            self.new_frog()
        else:
            car = util.detect_collision(self, cars, 2)
            if car:
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
                self.step(-1)
                self[key.LEFT] = False
            elif self[key.RIGHT]:
                self.rotation = 0
                self.start_moving()
                self.step(1)
                self[key.RIGHT] = False
            elif self[key.UP]:
                self.rotation = 90
                self.start_moving()
                self.jump(1)
                self[key.UP] = False
            elif self[key.DOWN]:
                self.rotation = -90
                self.start_moving()
                self.jump(-1)
                self[key.DOWN] = False
            self.check_position(dt, pads, cars, logs)
            if self.game.time_remaining.time_left < 0:
                out_of_time_sound.play()
                self.new_frog(out_of_time=True)
            if self.lives > -1:
                previous = self.animation_time
                self.animation_time -= dt
                if self.animation_time < 0:
                    # check to see if we are ending an animation sequence
                    if previous*self.animation_time < 0:
                        # adjust the image so that the horizontal position
                        # of the center stays the same
                        self.x += (-self.at_rest_image.width +
                                    self.moving_image.width)/2
                    if self.rotation in [0, 180]:
                        self.width = self.at_rest_image.width
                        self.height = self.at_rest_image.height
                    else:
                        self.width = self.at_rest_image.height
                        self.height = self.at_rest_image.width
                    util.draw_rotated(self, self.at_rest_image)
                else:
                    self.width = self.moving_image.width
                    self.height = self.moving_image.height
                    util.draw_rotated(self, self.moving_image)
        else:
            self.die(dt)

    def start_moving(self):
        previous = self.animation_time
        # animation lasts barely long enough to see it; since we determine
        # the end of animation by crossing 0, add a tiny offset
        # to avoid accidental equality to zero.
        self.animation_time = 1.0/20 + 0.000001
        if previous <= 0: # animation not in progress
            # adjust the image so that the horizontal position of the center
            # stays the same
            self.x += (self.at_rest_image.width - self.moving_image.width)/2
        if self.rotation in [0, 180]:
            self.width = self.moving_image.width
            self.height = self.moving_image.height
        else:
            self.width = self.moving_image.height
            self.height = self.moving_image.width
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
        n = self.lives
        x = self.world.width
        y = self.world.height + self.min_y
        while n > 0:
            x -= (big_frog.width + 10)
            big_frog.blit(x, y)
            n -= 1