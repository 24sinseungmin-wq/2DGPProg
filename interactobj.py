from pico2d import load_image, get_time, load_font, draw_rectangle,clamp
import math
import calculfuncs
import play_loop

from sdl2 import SDL_HINT_WINDOWS_NO_CLOSE_ON_ALT_F4

import play_loop
import world
from ui import Popup,addpopup

class Interactobj:
    obj_image=None
    def __init__(self,x=1200,y=300,r=32,pw=64,ph=64,pr=100,reverse=False,imagetype=0,price=[],give=[],text=[]):
        self.images()
        self.reverse=reverse
        self.blink_timer=0
        self.special_action = None
        self.x=x
        self.y=y
        self.r=r
        self.collisionchecked=[]
        self.imagetype=imagetype
        self.popup=[]
        self.popup_w,self.popup_h=pw,ph
        self.popup_r=pr
        self.feedback=[]
        self.collision=[]
        self.price=price
        self.give=give
        self.text=text
        self.typename="area"
        self.delete=False
        self.areatoggle=False
        if self.imagetype==0:
            self.frame=4
        elif self.imagetype==1:
            self.frame=7
        elif self.imagetype==2:
            self.frame=10
        else:
            self.frame=1

    def images(self):
        if Interactobj.obj_image is None:
            Interactobj.obj_image=load_image('shopobj.png')

    def update(self):
        dt = play_loop.frame_time
        #self.blink_timer -= dt
        dist_pow=(play_loop.knight.x-self.x)**2+(play_loop.knight.y-self.y)**2
        if dist_pow<=self.popup_r**2 and self.text!=[]:
            if not self.areatoggle:
                self.areatoggle=True
                if self.imagetype == 0:
                    self.frame = 5
                elif self.imagetype == 1:
                    self.frame = 8
                elif self.imagetype == 2:
                    self.frame = 11
                else:
                    self.frame = 1
                if len(self.popup) == 0:
                    added_popup=Popup(self.x,self.y+50,0,0,self.popup_w,self.popup_h,self.text)
                    self.popup.append(added_popup)
                    addpopup(added_popup)
                else:
                    self.popup[0].tw,self.popup[0].th=self.popup_w,self.popup_h
        else:
            if self.areatoggle:
                self.areatoggle=False
                if self.imagetype == 0:
                    self.frame = 4
                elif self.imagetype == 1:
                    self.frame = 7
                elif self.imagetype == 2:
                    self.frame = 10
                else:
                    self.frame = 1
            if len(self.popup)>0:
                for pop in self.popup:
                    pop.tw, pop.th = 0, 0
                    if pop.deleteready:
                        pop.delete = True
                        self.popup.remove(pop)

        if not self.delete:
            world.collidecheck(self, "knight", "knightinarea")

        for case in self.collision:
            if case[0] in self.collisionchecked:
                pass
            else:
                if case[0].typename == "knight":
                    current_hp,current_para,current_money=case[0].max_hp,case[0].max_paradox,case[0].money
                    priceflag=True
                    for thing in self.price:
                        if thing[0]=='money':
                            if current_money<thing[1]:
                                priceflag=False
                    if priceflag:
                        for thing in self.give:
                            if thing[0]=='max_hp':
                                case[0].max_hp+=thing[1]
                            elif thing[0]=='max_paradox':
                                case[0].max_paradox+=thing[1]
                            elif thing[0]=='attackdamage':
                                case[0].attackdamage+=thing[1]
                        self.price=[]
                        self.give=[]
                        self.text=[]
                    pass

            self.collision.remove(case)

    def draw(self):
        Interactobj.obj_image.clip_draw(int(self.frame%2) *64,int(self.frame/2)*64, 64, 64, int((self.x - play_loop.cam_x) / 2) * 2,int((self.y - play_loop.cam_y) / 2) * 2, 128, 128)

    def sendfeedback(self,fdbk):
        self.feedback.append(fdbk)

    def deleteaction(self):
        for pop in self.popup:
            pop.tw,pop.th=-1,-1
            pop.autodelete=True
        self.popup=[]
        pass