'''frog.py

Our hero!
'''
import os
from pyglet import image
from pyglet import media
from pyglet.window import key

import util

DIR = os.path.dirname(__file__)

img_filename = os.path.join(DIR, "images", 'frog.png')
frog_at_rest = image.load(img_filename)

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
        self.at_rest = frog_at_rest
        self.width = self.at_rest.width
        self.height = self.at_rest.height
        self.min_y = 5
        self.lives = 4
        self.dying = False
        self.sinking = False
        self.new_frog(new_life=False)

    def new_frog(self, new_life = True):
        self.lane = 0
        if new_life:
            self.lives -= 1
            self.dying = 1.01  # time for animation
            if self.lives < 0:
                self.game.over = True
            else:
                self.game.time_remaining.restart()
        else:
            self.x = (self.world.width - self.at_rest.width)/2
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
        if self.x < 0:
            self.x = 0
        elif self.x > self.world.width - self.at_rest.width:
            self.x -= dx

    def check_position(self, dt, pads, cars, logs):
        '''check to see if we reached a "winning" position'''
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
            log = util.detect_collision(self, logs)
            if not log:
                self.sinking = True
                splash_sound.play()
                self.new_frog()
            else:
                self.x += log.vx*dt
        else:
            car = util.detect_collision(self, cars)
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
                self.step(-1)
                self[key.LEFT] = False
            elif self[key.RIGHT]:
                self.step(1)
                self[key.RIGHT] = False
            elif self[key.UP]:
                self.jump(1)
                self[key.UP] = False
            elif self[key.DOWN]:
                self.jump(-1)
                self[key.DOWN] = False
            self.check_position(dt, pads, cars, logs)
            if self.game.time_remaining.time_left < 0:
                out_of_time_sound.play()
                self.new_frog()
            if self.lives > -1:
                self.at_rest.blit(self.x, self.y)
        else:
            self.die(dt)

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
            self.x = (self.world.width - self.at_rest.width)/2
            self.y = self.min_y

    def display_lives(self):
        n = self.lives
        x = self.world.width
        y = self.world.height + self.min_y
        while n > 0:
            x -= (self.width + 10)
            self.at_rest.blit(x, y)
            n -= 1