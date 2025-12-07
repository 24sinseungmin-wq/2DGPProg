from pico2d import load_image, get_time, load_font, draw_rectangle,clamp
import math
import play_loop

from sdl2 import SDL_HINT_WINDOWS_NO_CLOSE_ON_ALT_F4

import play_loop
import world
CANVAS_W=800
CANVAS_H=800

class Background:
    image_1=None
    #image_2=None
    def __init__(self,w=4000,h=4000,reverse=False,imagetype=0):
        self.images()
        self.w=w
        self.h=h
        self.frame=self.imagetype=imagetype
        self.typename="background"
        self.delete=False

    def images(self):
        if Background.image_1 is None:
            Background.image_1=load_image('background_1.png')
        #if Background.image_2 is None:
        #    Background.image_2=load_image('background_2.png')

    def update(self):
        pass

    def draw(self):
        Background.image_1.clip_draw(int((play_loop.cam_x+CANVAS_W/2)/2),int((play_loop.cam_y+CANVAS_H/2)/2), int(CANVAS_W/2), int(CANVAS_H/2), int(CANVAS_W/2),int(CANVAS_H/2), CANVAS_W, CANVAS_H)

    def sendfeedback(self,fdbk):
        pass

    def deleteaction(self):
        pass