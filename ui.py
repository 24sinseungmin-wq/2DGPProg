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
            if hasattr(o, 'delete'):
                if o.delete:
                    o.deletefunc()
                    layer.remove(o)

def addpopup(popup):
    ui[0].append(popup)

def uiinit(knight):
    for layer in ui:
        layer.clear()
    health_bar=Health_bar(knight,False)
    ui[1].append(health_bar)

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

class Popup(DefaultUI):
    bg_image_n=None
    bg_image_p=None
    text_image=None
    def __init__(self, x=0.0, y=0.0,w=0.0,h=0.0, tw=100.0, th=100.0, text=["P???P"], popup_type="Normal"):
        super().__init__(False)
        self.image()
        self.type=popup_type
        self.x,self.y=x,y
        self.tw,self.th=tw,th
        self.w,self.h=w,h
        self.text=text
        self.deleteready=False
        self.delete=False
        self.autodelete=False
        """
        0123456789-+:?HAPGabcde 
        """
    def image(self):
        if type=="Paradox" and Popup.bg_image_p is None:
            Popup.bg_image_p=load_image("paradox_popup.png")
        elif Popup.bg_image_n is None:
            Popup.bg_image_n=load_image("normal_popup.png")
        if Popup.text_image is None:
            Popup.text_image=load_image("tempfont.png")

    def draw(self):
        uix,uiy = int((self.x - play_loop.cam_x) / 2),int((self.y - play_loop.cam_y) / 2)
        bg_cxm=bg_cxp=int(uix)
        bg_cym = bg_cyp = int(uiy)
        bg_ew=int(self.w/2)
        bg_eh=int(self.h/2)
        bg_xm=int(uix)-int(self.w/2)
        bg_xp=int(uix)+int(self.w/2)
        bg_ym=int(uiy)-int(self.h/2)
        bg_yp=int(uiy)+int(self.h/2)
        if self.w>=16:
            bg_cxm=bg_xm+8
            bg_cxp=bg_xp-8
            bg_ew=8
        if self.h>=16:
            bg_cym=bg_ym+8
            bg_cyp=bg_yp-8
            bg_eh=8
        bg_xm+=bg_ew/2
        bg_ym+=bg_eh/2
        bg_cxp+=bg_ew/2
        bg_cyp+=bg_eh/2
        Popup.bg_image_n.clip_draw(8,8,16,16,int(uix)*2,int(uiy)*2,2*int(self.w),2*int(self.h))
        Popup.bg_image_n.clip_draw(0,0,bg_ew,bg_eh,bg_xm*2,bg_ym*2,2*bg_ew,2*bg_eh)
        Popup.bg_image_n.clip_draw(32-bg_ew,0,bg_ew,bg_eh,bg_cxp*2,bg_ym*2,2*bg_ew,2*bg_eh)
        Popup.bg_image_n.clip_draw(0,32-bg_eh,bg_ew,bg_eh,bg_xm*2,bg_cyp*2,2*bg_ew,2*bg_eh)
        Popup.bg_image_n.clip_draw(32-bg_ew,32-bg_eh,bg_ew,bg_eh,bg_cxp*2,bg_cyp*2,2*bg_ew,2*bg_eh)

        letter_y=bg_cyp-4
        if self.h>=8 and len(self.text)>0:
            for line in self.text:
                if len(line)==0 or letter_y<bg_cym: break
                letter_x=bg_cxm
                for letter in line:
                    if letter_x > bg_cxp: break
                    imy, imx = self.fontalign(letter)
                    Popup.text_image.clip_draw(8 * imx, 8 * imy, 8, 8, letter_x * 2, letter_y * 2, 16, 16)
                    letter_x += 8
                letter_y -= 8
    def update(self):
        dt=play_loop.frame_time
        if self.w!=self.tw: self.w=self.w*pow(0.05,dt)+self.tw*(1-pow(0.05,dt))
        if self.h!=self.th: self.h=self.h*pow(0.05,dt)+self.th*(1-pow(0.05,dt))
        if self.w>self.tw:
            self.w-=dt*10
            if self.w<self.tw:self.w=self.tw
        elif self.w<self.tw:
            self.w+=dt*10
            if self.w>self.tw:self.w=self.tw
        if self.h>self.th:
            self.h-=dt*10
            if self.h<self.th:self.h=self.th
        elif self.h<self.th:
            self.h+=dt*10
            if self.h>self.th:self.h=self.th
        if self.w<=0 and self.h<=0 and self.tw<=0 and self.th<=0:
            self.deleteready=True
        if self.deleteready and self.autodelete and not self.delete:
            self.delete=True
    def deletefunc(self):
        pass
    def fontalign(self,letter):
        if letter=="0": return 4,0
        if letter=="1": return 4,1
        if letter=="2": return 4,2
        if letter=="3": return 4,3
        if letter=="4": return 4,4
        if letter=="5": return 3,0
        if letter=="6": return 3,1
        if letter=="7": return 3,2
        if letter=="8": return 3,3
        if letter=="9": return 3,4
        if letter=="-": return 2,0
        if letter=="+": return 2,1
        if letter=="?": return 2,2
        if letter=="H": return 2,4
        if letter=="A": return 1,0
        if letter=="P": return 1,1
        if letter=="G": return 1,2
        if letter=="a": return 1,3
        if letter=="b": return 1,4
        if letter=="c": return 0,0
        if letter=="d": return 0,1
        if letter=="e": return 0,2
        if letter=="f": return 0,3
        if letter=="L": return 0,4
        if letter==" " : return 2,3