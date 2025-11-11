from pico2d import load_image, get_time, load_font, draw_rectangle
import math

from sdl2 import SDL_HINT_WINDOWS_NO_CLOSE_ON_ALT_F4

import play_loop
import world

class Monster:
    def __init__(self,x=1200,y=300,state="spawn",hp='null',reversed=False):
        self.images()
        self.max_hp=100
        if hp=='null':
            self.hp=self.max_hp
        else:
            self.hp=hp
        self.state=state
        self.face_dir=1
        self.state_timer=0
        self.frame=0
        self.x=x
        self.y=y
        self.vx=self.vy=0
        self.tx=self.ty=0
        self.r=48
        self.feedback=[]
        self.collision=[]
        self.collisionchecked=[]
        self.able_action=True
        self.reverse=reversed
        self.typename="monster"
        self.delete=False

    def images(self):
        pass

    def update(self):
        if self.reverse:
            self.update_reverse()
        else:
            self.update_normal()

    def update_normal(self):
        pass

    def update_reverse(self):
        pass

    def degreeintofacedir(self,degree):
        dirresult = 0
        dirx = -math.sin(degree)
        diry = -math.cos(degree)
        if (degree >= -math.pi / 4 and degree < math.pi / 4):
            dirresult = 3
        elif (degree >= math.pi / 4 and degree < (3 * math.pi) / 4):
            dirresult = 0
        elif (degree >= (3 * math.pi) / 4 or degree < -(3 * math.pi) / 4):
            dirresult = 2
        elif (degree >= (-3 * math.pi) / 4 and degree < -math.pi / 4):
            dirresult = 1
        return dirx,diry,dirresult

    def facedirection(self, x, y, tx, ty):
        tempdir = math.atan2(x - tx, y - ty)
        dirx = -math.sin(tempdir)
        diry = -math.cos(tempdir)
        dirresult = 0
        if (tempdir >= -math.pi / 4 and tempdir < math.pi / 4):
            dirresult = 3
        elif (tempdir >= math.pi / 4 and tempdir < (3 * math.pi) / 4):
            dirresult = 0
        elif (tempdir >= (3 * math.pi) / 4 or tempdir < -(3 * math.pi) / 4):
            dirresult = 2
        elif (tempdir >= (-3 * math.pi) / 4 and tempdir < -math.pi / 4):
            dirresult = 1
        return dirx, diry, dirresult, tempdir

    def facedirection2(self, tx, ty):
        tempdir = math.atan2(tx, ty)
        dirx = -math.sin(tempdir)
        diry = -math.cos(tempdir)
        dirresult = 0
        if (tempdir >= -math.pi / 4 and tempdir < math.pi / 4):
            dirresult = 3
        elif (tempdir >= math.pi / 4 and tempdir < (3 * math.pi) / 4):
            dirresult = 0
        elif (tempdir >= (3 * math.pi) / 4 or tempdir < -(3 * math.pi) / 4):
            dirresult = 2
        elif (tempdir >= (-3 * math.pi) / 4 and tempdir < -math.pi / 4):
            dirresult = 1
        return dirresult, tempdir

    #def draw(self)