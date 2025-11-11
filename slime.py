from pico2d import load_image, get_time, load_font, draw_rectangle
import math
import random
from monsterbase import Monster

from sdl2 import SDL_HINT_WINDOWS_NO_CLOSE_ON_ALT_F4

import play_loop
import world

FAINT_TIME=0.5

class Slime(Monster):
    jump_image=None
    move_image=None
    hit_image=None
    def __init__(self,x=1200,y=300,state="spawn",hp='null',reversed=False):
        super().__init__(x,y,state,hp,reversed)
        self.max_hp=20
        if self.hp>self.max_hp:
            self.hp=self.max_hp
        self.movespeed=1
        self.state=state
        self.face_dir=1
        self.dir_rot=0
        self.state_timer=0
        self.idle_timer=0
        self.frame=0
        self.x=x
        self.y=y
        self.r=18
        self.vx=self.vy=0
        self.tx=self.ty=0
        self.able_action=True

    def images(self):
        if Slime.jump_image==None:
            Slime.jump_image=load_image('slime_jump.png')
        if Slime.move_image==None:
            Slime.move_image=load_image('slime_move.png')
        #Slime.hit_image

    def update_normal(self):
        dt = play_loop.frame_time

        self.collisionchecked=[]
        world.collidecheck(self,"knight","collidewithenemy")
        world.collidecheck(self,"monster","collidewithteam")
        for case in self.collision:
            if case[0] in self.collisionchecked:
                pass
            else:
                if case[0].typename=="knight":
                    pass
                elif case[0].typename=="monster":
                    tempdist=math.sqrt((self.x-case[0].x)**2+(self.y-case[0].y)**2)
                    tempvx,tempvy,temp,temp=self.facedirection(self.x,self.y,case[0].x,case[0].y)
                    kbdist=(tempdist-self.r-case[0].r)**2
                    self.vx+=tempvx*kbdist*dt
                    self.vy+=tempvy*kbdist*dt
                    pass
            self.collision.remove(case)

        for fdbk in self.feedback:
            if fdbk[0]=="despawn":
                self.delete=True
                self.frame = 0
            elif fdbk[0]=="damage":
                #공격자(fdbk[1]에게 자신을 포함한 정보 전달)?
                self.hp-=fdbk[2]
                if self.hp<=0:
                    self.state="death"
                    self.state_timer=0
            elif fdbk[0]=="knockback_hit":
                if self.state!='hit':
                    self.hp -= fdbk[2]
                    self.vx += fdbk[3]
                    self.vy += fdbk[4]
                    #공격자(fdbk[1]에게 자신을 포함한 정보 전달)
                    if self.hp<=0:
                        self.state = "death"
                    else:
                        self.face_dir,temp1=self.facedirection2(fdbk[2],fdbk[3])
                        self.state = "hit"
                    self.able_action=False
                    self.state_timer=0
                    self.frame = 0
            self.feedback.remove(fdbk)

        if self.state=='spawn':
            self.state='idle'
            self.state_timer=0
        elif self.state=='idle':
            self.idle_timer-=dt
            self.x+=self.vx
            self.y+=self.vy
            self.vx*=pow(0.01,dt)
            self.vy*=pow(0.01,dt)
            if self.idle_timer<=0:
                self.idle_timer=0
                tx,ty=play_loop.knight.x,play_loop.knight.y
                dist=math.sqrt((self.x-tx)**2+(self.y-ty)**2)
                if dist<1000:
                    self.vx,self.vy,temp1,tempdeg=self.facedirection(self.x,self.y,tx,ty)
                    self.vx,self.vy,self.face_dir=self.degreeintofacedir(tempdeg+math.radians(((2*random.random()-1)**2)*30))
                    dashdist=self.movespeed*(0.6+(random.random()**2)*0.4)
                    self.vx*=dashdist
                    self.vy *= dashdist
                    self.state='move'
                    self.state_timer=0
                    self.frame=0
                pass
        elif self.state=='hit':
            self.state_timer+=dt
            self.x+=self.vx
            self.y+=self.vy
            self.vx*=pow(0.1,dt)
            self.vy*=pow(0.1,dt)
            if self.state_timer>FAINT_TIME:
                self.idle_timer=0.3
                self.able_action=True
                self.state='idle'
        elif self.state=='move':
            self.state_timer+=dt
            self.frame=(self.state_timer*4/0.4)
            if self.frame>3:self.frame=3
            self.x+=self.vx
            self.y+=self.vy
            self.vx*=pow(0.075,dt)
            self.vy*=pow(0.075,dt)
            if self.state_timer>0.5:
                self.state='idle'
                self.idle_timer=0.75+0.5*(random.random()**2)
                self.able_action=True
                self.frame=0
                self.state_timer=0
        elif self.state=='jump':
            self.state_timer+=dt
            if self.state_timer<=0.25:
                self.frame=(self.state_timer*4/0.25)
            elif self.state_timer<=0.75:
                self.frame=3
            elif self.state_timer<=1.25:
                self.frame=3+((self.state_timer-0.75)*6/0.5)
            else:
                self.state='idle'
                self.idle_timer=0.75
                self.able_action=True
                self.frame=0
                self.state_timer=0
        pass

    def draw(self):
        if self.state=='idle':
            Slime.jump_image.clip_draw(0, 0, 32, 32,int((self.x - play_loop.cam_x) / 3) * 3,int((self.y - play_loop.cam_y) / 3) * 3 + 12, 96, 96)
        elif self.state=='move':
            Slime.move_image.clip_draw((int(self.frame) % 4) * 32, self.face_dir * 32, 32, 32,int((self.x - play_loop.cam_x) / 3) * 3,int((self.y - play_loop.cam_y) / 3) * 3 + 12, 96, 96)
        elif self.state=='jump':
            Slime.jump_image.clip_draw(0,int(self.frame) * 32, 32, 32,int((self.x - play_loop.cam_x) / 3) * 3,int((self.y - play_loop.cam_y) / 3) * 3 + 12, 96, 96)
