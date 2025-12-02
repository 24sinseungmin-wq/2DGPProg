from pico2d import load_image, get_time, load_font, draw_rectangle
import math

from sdl2 import SDL_HINT_WINDOWS_NO_CLOSE_ON_ALT_F4

import play_loop
import interface
import world
from shadow import Shadow

STAGGER_TIME=0.75

class Knight:
    def __init__(self):
        self.attack_image = load_image('knight_attack.png')
        self.walk_image = load_image('knight_walk.png')
        self.max_hp=6
        self.hp=6
        self.max_paradox=9
        self.paradox=0
        self.iframe=0
        self.paradox_iframe=0
        self.walkspeed=200
        self.attackspeed=3000
        self.attackdamage=5
        self.attackrange=100
        self.state="walking"
        self.face_dir=1
        self.state_timer=0
        self.frame=0
        self.x=0
        self.y=0
        self.r=15
        self.vx=self.vy=self.dmgvx=self.dmgvy=0
        self.order=[]
        self.collision=[]
        self.tx=self.ty=0
        self.action='none'
        self.able_action=True
        self.able_walk=True
        self.typename="knight"
        self.delete=False
        self.staggerflag=False
        self.paradox_damage_flag=False
        self.damage_hp_reserved=0
        self.damage_paradox_reserved=0
        self.areas=[]
        self.para_x=0
        self.para_y=0
        self.para_r=1000
        self.shadow=Shadow(self.x,self.y,0)
        world.add_object(self.shadow,5)

    def damageknockback(self,hp_dmg,paradox_dmg,vx,vy):
        if self.action!='attacking' and self.iframe<=0:
            self.staggerflag=True
            self.damage_hp_reserved=hp_dmg
            self.damage_paradox_reserved=paradox_dmg
            self.dmgvx=vx
            self.dmgvy=vy

    def damage_ignore_iframe(self,paradox_dmg):
        self.paradox+=paradox_dmg
        self.paradox_damage_flag=True

    def set_parapos(self,x,y,r):
        self.para_x=x
        self.para_y=y
        self.para_r=r

    def parapos_check(self,x,y,r):
        return ((self.para_x-x)**2+(self.para_y-y)**2)<=(r+self.para_r)**2

    def update(self):
        #interface에서 들어온 명령 받음
        for command in self.order:
            if command[0]=='faceto':
                self.tx=command[1]
                self.ty=command[2]
                if self.state=="walking":
                    self.vx,self.vy,self.face_dir=self.facedirection(self.x,self.y,self.tx,self.ty)
                    self.vx *= self.walkspeed
                    self.vy *= self.walkspeed
                elif self.able_action:
                    temp1, temp2, self.face_dir = self.facedirection(self.x, self.y, self.tx, self.ty)
                pass

            if command[0]=='startstepto':
                if self.able_action and self.able_walk:
                    self.tx = command[1]
                    self.ty = command[2]
                    self.action=command[0]
                    self.vx, self.vy, self.face_dir = self.facedirection(self.x, self.y, self.tx, self.ty)
                    self.vx*=self.walkspeed
                    self.vy*=self.walkspeed
                    if self.state != 'walking':
                        self.state='walking'
                        self.frame=0
                pass

            elif command[0]=='attackcharge':
                if self.able_action:
                    self.able_walk=False
                    self.state='attack_charge'
                    temp1, temp2, self.face_dir = self.facedirection(self.x, self.y, self.tx, self.ty)
                    self.tx = command[1]
                    self.ty = command[2]
                    self.action=command[0]
                    self.frame=0
                pass

            elif command[0]=='attackrelease':
                if self.able_action and self.state=='attack_charge':
                    if self.state_timer>=0.5:
                        self.able_action=False
                        self.state='attacking'
                        self.iframe=0.1
                        self.frame=0
                        self.state_timer=0
                        self.tx = command[1]
                        self.ty = command[2]
                        self.action=command[0]
                        self.vx,self.vy,self.face_dir=self.facedirection(self.x,self.y,self.tx,self.ty)
                        self.vx *= self.attackspeed
                        self.vy *= self.attackspeed
                        particle=Swordeffect(self)
                        if self.face_dir==1 or self.face_dir==3:
                            world.add_object(particle, 7)
                        else:
                            world.add_object(particle,9)
                    else:
                        if interface.toggleR:
                            self.state = 'walking'
                        else:
                            self.state = 'idle'
                        self.frame=0
                        self.state_timer=0
                pass
            elif command[0]=='idle':
                if self.able_action:
                    self.able_walk=True
                    self.state='idle'
                    self.frame=0
                pass
            elif command[0]=='none':
                pass
            else:
                pass
            self.order.remove(command)

        dt=play_loop.frame_time

        self.iframe -= dt
        self.para_x=self.para_x*pow(0.95,dt)+self.x*(1-pow(0.95,dt))
        self.para_y=self.para_y*pow(0.95,dt)+self.y*(1-pow(0.95,dt))
        #state별 계산
        if self.state=="walking":
            self.frame = (self.frame+dt/0.10)%4
            self.x+=self.vx*dt
            self.y+=self.vy*dt
            while self.para_r<1000:
                self.para_r+=self.walkspeed*dt
            if (self.tx-self.x)*self.vx<=0:
                self.state='idle'
                self.frame=0
                self.state_timer=0

        elif self.state=="idle":
            self.vx*=pow(0.02,dt)
            self.vy*=pow(0.02,dt)
            while self.para_r<1000:
                self.para_r+=self.walkspeed*dt
            #self.vx,self.vy 감쇄

        elif self.state=="attack_charge":
            self.state_timer+=dt
            self.frame = (self.state_timer * 2 / 0.5)
            if self.frame>2:
                self.frame=2

        elif self.state=="attacking":
            self.frame = (self.frame+dt*10)
            self.state_timer+=dt
            if self.frame>2:
                self.frame=2
            if (self.tx-self.x)*self.vx>=0:
                self.x += self.vx * dt
                self.y += self.vy * dt
                while self.para_r < 1000:
                    self.para_r += math.sqrt(self.vx ** 2 + self.vy ** 2)*dt
                world.damagecolide(self.attackdamage, self.x, self.y, self.x + self.vx * dt, self.y + self.vy * dt, self.attackrange,0.03, 0.03, "monster", self)
            if self.state_timer>=0.1:
                self.state="attack_cooldown"
                self.iframe=0.2
                self.frame=0
                self.state_timer=0

        elif self.state=="attack_cooldown":
            self.state_timer+=dt
            if self.state_timer<=0.2:
                self.frame=0
            else:
                self.frame = (self.frame + dt/0.1)
            self.vx=0
            self.vy=0
            #self.x+=self.vx*dt
            #self.y+=self.vy*dt
            #self.vx*=pow(0.001,dt)
            #self.vy*=pow(0.001,dt)
            if self.frame>4:
                self.frame=4
            if self.state_timer>0.6:
                self.frame=0
                self.state_timer=0
                self.able_action=True
                self.able_walk=True
                if interface.toggleR:
                    self.state = 'walking'
                else:
                    self.state = 'idle'

        elif self.state=="stagger":
            self.state_timer+=dt
            self.x+=self.vx*dt
            self.y+=self.vy*dt
            while self.para_r<1000:
                self.para_r+=(math.sqrt(self.vx**2+self.vy**2)+0.1)*dt
            self.vx*=pow(0.02,dt)
            self.vy*=pow(0.02,dt)
            if self.state_timer>STAGGER_TIME:
                self.state='idle'
                self.able_action=True
                self.state_timer=0

        if self.staggerflag:
            if self.state!='attacking' and self.iframe<=0:
                print("knight hit!")
                self.state = 'stagger'
                self.frame = 0
                self.able_action = False
                self.state_timer = 0
                self.iframe = 1.5
                self.hp -= self.damage_hp_reserved
                self.hp -= self.damage_paradox_reserved
                self.vx,self.vy=self.dmgvx,self.dmgvy
                self.damage_hp_reserved = self.damage_paradox_reserved = 0
            self.staggerflag=False
        self.shadow.x,self.shadow.y=self.x,self.y

    def control(self,action,x,y):
        self.order.append((action,x,y))

    def facedirection(self,x,y,tx,ty):
        tempdir = math.atan2(x-tx,y-ty)
        dirx=-math.sin(tempdir)
        diry=-math.cos(tempdir)
        dirresult=0
        if (tempdir>=-math.pi/4 and tempdir<math.pi/4):
            dirresult=3
        elif (tempdir>=math.pi/4 and tempdir<(3*math.pi)/4):
            dirresult=0
        elif (tempdir>=(3*math.pi)/4 or tempdir<-(3*math.pi)/4):
            dirresult=2
        elif (tempdir>=(-3*math.pi)/4 and tempdir<-math.pi/4):
            dirresult=1
        return dirx,diry,dirresult

    def draw(self):
        if self.state=="walking":
            self.walk_image.clip_draw((int(self.frame)%4)*32,self.face_dir*32,32,32,int((self.x-play_loop.cam_x)/2)*2,int((self.y-play_loop.cam_y)/2)*2+32,64,64)
        elif self.state == "attack_charge" or self.state=="idle" or self.state=="stagger":
            self.attack_image.clip_draw((int(self.frame) % 10) * 32, self.face_dir * 32, 32, 32, int((self.x-play_loop.cam_x)/2)*2, int((self.y-play_loop.cam_y)/2)*2+32,64,64)
        elif self.state == "attacking":
            self.attack_image.clip_draw((3+int(self.frame) % 3) * 32, (self.face_dir) * 32, 32, 32, int((self.x-play_loop.cam_x)/2)*2, int((self.y-play_loop.cam_y)/2)*2+32,64,64)
        elif self.state == "attack_cooldown":
            self.attack_image.clip_draw((5+int(self.frame) % 5) * 32, (self.face_dir) * 32, 32, 32, int((self.x-play_loop.cam_x)/2)*2, int((self.y-play_loop.cam_y)/2)*2+32,64,64)

    def deleteaction(self):
        if not self.shadow==None:
            self.shadow.delete=True

class Swordeffect:
    image_1=None
    def __init__(self,knight,type=0,dir=0):
        self.knight=knight
        self.x=self.knight.x
        self.y=self.knight.y
        self.vx=self.knight.vx*1.1
        self.vy=self.knight.vy*1.1
        self.dir=dir
        self.state_timer=0
        self.frame=0
        self.typename="particle"
        self.delete=False
        self.areas=[]
        if type==0:
            self.dir=self.knight.face_dir
            if Swordeffect.image_1 == None:
                Swordeffect.image_1=load_image('knight_attack_effect.png')
    def update(self):
        dt=play_loop.frame_time
        self.state_timer+=dt
        if self.knight.state=="attacking":
            self.x = self.knight.x
            self.y = self.knight.y
        self.frame=(self.state_timer*4*4)
        if self.frame>4: self.frame=4
        if self.state_timer>0.25:
            self.delete=True
    def draw(self):
        Swordeffect.image_1.clip_draw((int(self.frame) % 4) * 64, (self.dir) * 64, 64, 64, int((self.x-play_loop.cam_x)/ 3) * 3, int((self.y-play_loop.cam_y) / 3) * 3 + 32, 192, 192)
    def deleteaction(self):
        pass