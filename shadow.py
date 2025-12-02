from pico2d import load_image, get_time, load_font, draw_rectangle
import math

from sdl2 import SDL_HINT_WINDOWS_NO_CLOSE_ON_ALT_F4

import play_loop

class Shadow:
    image1=None
    def __init__(self,x=600,y=300,shadowtype=0):
        self.shadowtype=shadowtype
        self.images()
        self.x=x
        self.y=y
        self.typename="shadow"
        self.delete=False
        self.areas=[]

    def images(self):
        if self.shadowtype==0 and Shadow.image1==None:
            Shadow.image1=load_image('shadow_small.png')

    def update(self):
        pass

    def draw(self):
        if self.shadowtype==0:
            Shadow.image1.clip_draw(0,0, 32, 32, int((self.x-play_loop.cam_x)/ 2) * 2, int((self.y-play_loop.cam_y) / 2) * 2, 64, 64)

    def deleteaction(self):
        pass