from pico2d import load_image, get_time, load_font, draw_rectangle
import math

from sdl2 import SDL_HINT_WINDOWS_NO_CLOSE_ON_ALT_F4

import play_loop
import interface

#player=play_loop.knight
ui=[[] for _ in range(4)]   #HP 바 등/HP 등/팝업창/팝업창 위

HPBAR_X,HPBAR_Y=0,64
HPBAR_ICONGAP=9*2
ANIM_SPEED=0.6

def render():
    for layer in ui:
        for o in layer:
            if not o.hidden:
                o.draw()

def update():
    for layer in ui:
        for o in layer:
            if not o.hidden:
                o.update()

def uiinit(knight):
    for layer in ui:
        layer.clear()
    health_bar=Health_bar(knight,False)
    ui[0].append(health_bar)

class DefaultUI:
    def __init__(self,hidden=True):
        self.hidden=hidden
        self.images()
    def images(self):
        pass
    def draw(self):
        pass

class Health_bar(DefaultUI):
    icon=None
    def __init__(self,knight,hidden=False):
        super().__init__(hidden)
        self.knight=knight
        self.reversed=False
        self.icons=[{'type':'none','to_type':'none','frame':0} for i in range(10)]
        self.hp=knight.hp
        self.max_hp=knight.max_hp
        self.paradox=knight.paradox
        self.max_paradox=knight.max_paradox
        self.xdelta=15
        self.length=30

    def images(self):
        if Health_bar.icon==None:
            Health_bar.icon=load_image('shield_big_icon.png')

    def draw(self):

        for num in range(len(self.icons)):
            if num*2<self.knight.hp:
                if self.knight.hp-num*2==1:
                    self.icons[num]['to_type']='half_shield'
                else:
                    self.icons[num]['to_type']='full_shield'
            elif num*2<self.knight.max_hp:
                self.icons[num]['to_type']='empty_shield'
            elif num*6<3*self.knight.max_hp+2*(self.knight.max_paradox-self.knight.paradox):
                if int(self.knight.max_hp*1.5+(self.knight.max_paradox-self.knight.paradox)-num*3)<=1:
                    self.icons[num]['to_type']='one_third_paradox'
                elif int(self.knight.max_hp*1.5+(self.knight.max_paradox-self.knight.paradox)-num*3)<=2:
                    self.icons[num]['to_type']='two_third_paradox'
                else:
                    self.icons[num]['to_type']='full_paradox'
            elif num*6<3*self.knight.max_hp+2*self.knight.max_paradox:
                self.icons[num]['to_type'] = 'empty_paradox'
            else:
                self.icons[num]['to_type'] = 'none'

            frame_x=-1
            frame_y=-1

            if self.icons[num]['to_type']=='empty_shield':
                if self.icons[num]['type']=='empty_shield':
                    frame_x,frame_y=5,0
                elif self.icons[num]['type']=='none':
                    frame_x,frame_y=self.icons[num]['frame'],0
                elif self.icons[num]['type']=='half_shield' or  self.icons[num]['type']=='full_shield':
                    frame_x,frame_y=self.icons[num]['frame'],2
                else:
                    self.icons[num]['frame']=-1
                    self.icons[num]['type']='empty_shield'
                    frame_x,frame_y=5,0
            elif self.icons[num]['to_type']=='half_shield':
                if self.icons[num]['type']=='half_shield':
                    frame_x,frame_y=5,1
                elif self.icons[num]['type']=='full_shield':
                    frame_x,frame_y=self.icons[num]['frame'],1
                elif self.icons[num]['type']=='empty_shield':
                    frame_x,frame_y=self.icons[num]['frame'],3
                else:
                    self.icons[num]['frame']=-1
                    self.icons[num]['type']='half_shield'
                    frame_x,frame_y=5,1
            elif self.icons[num]['to_type']=='full_shield':
                if self.icons[num]['type']=='full_shield':
                    frame_x,frame_y=5,4
                elif self.icons[num]['type']=='half_shield':
                    frame_x,frame_y=self.icons[num]['frame'],4
                elif self.icons[num]['type']=='empty_shield':
                    if self.icons[num]['frame']<=4:
                        frame_x, frame_y = 5 - self.icons[num]['frame'], 2
                    else:
                        frame_x, frame_y = 5,4
                else:
                    self.icons[num]['frame']=-1
                    self.icons[num]['type']='full_shield'
                    frame_x,frame_y=5,4
            elif self.icons[num]['to_type']=='full_paradox':
                if self.icons[num]['type']=='full_paradox':
                    frame_x,frame_y=5,5
                elif self.icons[num]['type']=='none':
                    frame_x,frame_y=self.icons[num]['frame'],5
                elif self.icons[num]['type']=='empty_shield' or self.icons[num]['type']=='half_shield' or self.icons[num]['type']=='full_shield':
                    frame_x,frame_y=self.icons[num]['frame'],6
                #elif self.icons[num]['type']=='empty_paradox':
                else:
                    self.icons[num]['frame']=-1
                    self.icons[num]['type']='full_paradox'
                    frame_x,frame_y=5,5
            elif self.icons[num]['to_type']=='two_third_paradox':
                if self.icons[num]['type']=='two_third_paradox':
                    frame_x,frame_y=5,7
                elif self.icons[num]['type']=='full_paradox':
                    frame_x,frame_y=self.icons[num]['frame'],7
                elif self.icons[num]['type']=='one_third_paradox' or self.icons[num]['type']=='empty_paradox':
                    frame_x,frame_y=self.icons[num]['frame'],7
                else:
                    frame_x,frame_y=self.icons[num]['frame'],7
            elif self.icons[num]['to_type']=='one_third_paradox':
                if self.icons[num]['type']=='one_third_paradox':
                    frame_x,frame_y=5,8
                elif self.icons[num]['type']=='full_paradox':
                    frame_x,frame_y=self.icons[num]['frame'],8
                elif self.icons[num]['type']=='two_third_paradox' or self.icons[num]['type']=='empty_paradox':
                    frame_x,frame_y=self.icons[num]['frame'],8
                else:
                    frame_x,frame_y=self.icons[num]['frame'],8
            elif self.icons[num]['to_type']=='empty_paradox':
                if self.icons[num]['type']=='empty_paradox':
                    frame_x,frame_y=5,9
                elif self.icons[num]['type']=='one_third_paradox' or self.icons[num]['type']=='two_third_paradox' or self.icons[num]['type']=='full_paradox':
                    frame_x,frame_y=self.icons[num]['frame'],9
                else:
                    self.icons[num]['frame']=5
                    self.icons[num]['type']='empty_paradox'
                    frame_x, frame_y = 5, 9
            elif self.icons[num]['to_type']=='none':
                if self.icons[num]['type']=='full_paradox':
                    frame_x,frame_y=5-self.icons[num]['frame'],5
                elif self.icons[num]['type']=='empty_shield':
                    frame_x,frame_y=self.icons[num]['frame'],0
                else:
                    self.icons[num]['frame']=-1
                    self.icons[num]['type']='none'
            else:
                self.icons[num]['frame']=-1
                self.icons[num]['type']=self.icons[num]['to_type']='none'

            if frame_x!=-1 and frame_y!=-1:
                uix=int(self.knight.x/2)*2+HPBAR_X-int(play_loop.cam_x/2)*2+num*18-int(self.xdelta/2)*2
                uiy=int(self.knight.y/2)*2+HPBAR_Y-int(play_loop.cam_y/2)*2
                Health_bar.icon.clip_draw(int(frame_x)*32,int(9-frame_y)*32, 32, 32, int(uix),int(uiy), 64, 64) #y좌표 쪽으로 1픽셀 덜덜이 해결할 것
        self.update()

    def update(self):
        dt=play_loop.frame_time
        for num in range(len(self.icons)):
            if self.icons[num]['type']!=self.icons[num]['to_type']:
                if self.icons[num]['frame']>=5:
                    self.icons[num]['type']=self.icons[num]['to_type']
                    self.icons[num]['frame']=-1
                else:
                    if self.icons[num]['frame']==-1:
                        self.icons[num]['frame']=0
                    else:
                        self.icons[num]['frame']+=dt*ANIM_SPEED*8
                if self.icons[num]['frame']>5:
                    self.icons[num]['frame']=5

        uibarlen = -HPBAR_ICONGAP
        uialllen = -HPBAR_ICONGAP

        for icon in self.icons:
            if not icon['type'] == icon['to_type'] == 'none':
                if icon['frame'] != -1:
                    if icon['type'] == 'none':
                        pass
                    elif icon['type'] == 'full_paradox' or icon['type'] == 'two_third_paradox' or icon[
                        'type'] == 'one_third_paradox' or icon['type'] == 'empty_paradox':
                        uialllen += HPBAR_ICONGAP
                    else:
                        uibarlen += HPBAR_ICONGAP
                        uialllen += HPBAR_ICONGAP
                else:
                    if icon['to_type'] == 'none':
                        pass
                    elif icon['to_type'] == 'full_paradox' or icon['to_type'] == 'two_third_paradox' or icon[
                        'to_type'] == 'one_third_paradox' or icon['to_type'] == 'empty_paradox':
                        uialllen += HPBAR_ICONGAP
                    else:
                        uibarlen += HPBAR_ICONGAP
                        uialllen += HPBAR_ICONGAP

        self.xdelta = (0.1 ** dt) * self.xdelta + (1 - 0.1 ** dt) * (uibarlen)/2
        if (self.xdelta-(uibarlen)/2)**2<0.5:
            self.xdelta=(uibarlen)/2
        self.length = (0.1 ** dt) * uialllen + (1 - 0.1 ** dt) * (uialllen-0.6)
        if (self.length-uialllen+0.6)**2<0.5:
            self.length=uialllen-0.6



