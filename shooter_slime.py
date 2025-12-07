from pico2d import load_image, get_time, load_font, draw_rectangle
import math
import random
from monsterbase import Monster
import calculfuncs
from area import Area
from shadow import Shadow

from sdl2 import SDL_HINT_WINDOWS_NO_CLOSE_ON_ALT_F4

import play_loop
import world

FAINT_TIME=1
#MAX_KB_SPEED=20
SHOOT_DIST_MAX=350
SHOOT_DIST_MIN=250
EXTRA_PARADOX_TIME=1.5

class Shooter_Slime(Monster):
    shoot_image=None
    move_image=None
    hit_image=None
    teleport_image=None
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
        self.iframe=0
        self.rand_wait=0
        self.rand_wait_idle=0
        self.frame=0
        self.x=x
        self.y=y
        self.height=0
        self.sx=self.sy=0
        self.tx=self.ty=0
        self.r=12
        self.vx=self.vy=0
        self.vbx=self.vby=0
        self.vfx=self.vfy=0
        self.vf=False
        self.able_action=True
        self.hpareaflag=False
        self.areas=[]
        self.proj=[]
        self.projflag=False

        self.shadow=None
        self.shadow=Shadow(self.x,self.y,0)
        world.add_object(self.shadow,5)

    def images(self):
        if Shooter_Slime.shoot_image==None:
            Shooter_Slime.shoot_image=load_image('shooterslime_shoot.png')
        if Shooter_Slime.move_image==None:
            Shooter_Slime.move_image=load_image('shooterslime_move.png')
        if Shooter_Slime.teleport_image==None:
            Shooter_Slime.teleport_image=load_image('shooterslime_teleport.png')
        #Shooter_Slime.hit_image

    def feedbackcheck(self):
        for fdbk in self.feedback:
            if fdbk[0]=="despawn":
                self.delete=True
                self.frame = 0
            elif fdbk[0]=="damage":
                #공격자(fdbk[1]에게 자신을 포함한 정보 전달)?
                if self.iframe==0 and self.height==0:
                    if self.reverse:
                        self.hp += fdbk[2]
                    else:
                        self.hp -= fdbk[2]
                    print(f'Slime hit! hp={self.hp}')

                    if self.hp <= 0:
                        self.hp = 0
                        if not self.reverse:
                            self.state = "death"
                        timer = 0
                        pass
                        # self.state="death"
                        # self.state_timer=0
                    if self.hp >self.max_hp:
                        self.hp=self.max_hp
            elif fdbk[0]=="knockback_hit":
                if self.state!='stagger' and self.height==0:
                    if reversed:
                        self.vfx = -fdbk[2]
                        self.vfy = -fdbk[3]
                        for area in self.areas:
                            area.delete = True
                        for p in self.proj:
                            p.delete = True
                            if p.shadow!=None:
                                p.shadow.delete = True
                    else:
                        self.vfx = fdbk[2]
                        self.vfy = fdbk[3]
                    self.vf = True
                    self.face_dir, temp1 = self.facedirection2(fdbk[2], fdbk[3])
                    self.state = "stagger"
                    self.iframe=FAINT_TIME
                    self.able_action = False
                    self.state_timer = 0
                    self.frame = 0
            self.feedback.remove(fdbk)

    def update_normal(self):
        dt = play_loop.frame_time
        self.collisionchecked=[]
        self.feedbackcheck()

        for p in self.proj:
            if p.deleteready:
                p.delete=True
                self.proj.remove(p)

        if self.iframe>0:
            self.iframe-=dt
            if self.iframe<0:
                self.iframe=0
        if self.state=='spawn':
            self.state='idle'
            self.state_timer=1.0
        elif self.state=='idle':
            self.idle_timer-=dt
            self.x+=self.vx
            self.y+=self.vy
            self.vx*=pow(0.05,dt)
            self.vy*=pow(0.05,dt)

            if self.idle_timer<=0:
                self.idle_timer=0
                tx,ty=play_loop.knight.x,play_loop.knight.y
                dist=math.sqrt((self.x-tx)**2+(self.y-ty)**2)
                if dist<SHOOT_DIST_MIN:
                    self.vx,self.vy,temp1,tempdeg=self.facedirection(tx,ty,self.x,self.y)
                    randegr=(random.random()-0.5)*math.radians(60)
                    self.vx,self.vy,self.face_dir=self.degreeintofacedir(tempdeg+randegr)
                    dashdist=self.movespeed*(0.6+(random.randint(0,20)**2)*0.001)
                    self.vx *= dashdist
                    self.vy *= dashdist
                    self.state='move'
                    self.state_timer=0
                    self.frame=0
                elif dist<=SHOOT_DIST_MAX:
                    if random.randint(0,1):
                        self.vy, self.vx, temp1, tempdeg = self.facedirection(self.x, self.y, tx, ty)
                        randegr = (random.random() - 0.5) * math.radians(20)
                        self.vy, self.vx, self.face_dir = self.degreeintofacedir(tempdeg + randegr)
                        dashdist = self.movespeed * (0.6 + (random.randint(0, 20) ** 2) * 0.001)
                        self.vx *= dashdist
                        self.vy *= dashdist
                        self.state = 'move'
                        self.state_timer = 0
                        self.frame = 0
                    else:
                        self.state = 'shoot'
                        self.state_timer = 0
                        self.frame = 0
                        self.projflag = False
                elif dist<=1000:
                    self.vx,self.vy,temp1,tempdeg=self.facedirection(self.x,self.y,tx,ty)
                    randegr=(random.random()-0.5)*math.radians(60)
                    self.vx,self.vy,self.face_dir=self.degreeintofacedir(tempdeg+randegr)
                    dashdist=self.movespeed*(0.6+(random.randint(0,20)**2)*0.001)
                    self.vx *= dashdist
                    self.vy *= dashdist
                    self.state='move'
                    self.state_timer=0
                    self.frame=0
                else:
                    randegr=(random.random()-0.5)*math.radians(360)
                    self.vx,self.vy,self.face_dir=self.degreeintofacedir(randegr)
                    dashdist=self.movespeed*(0.3+(random.randint(0,20)**2)*0.0005)
                    self.vx *= dashdist
                    self.vy *= dashdist
                    self.state='move'
                    self.state_timer=0
                    self.frame=0
        elif self.state=='stagger':
            self.state_timer+=dt
            self.x+=self.vx
            self.y+=self.vy
            self.vx*=pow(0.05,dt)
            self.vy*=pow(0.05,dt)
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
            self.vx*=pow(0.05,dt)
            self.vy*=pow(0.05,dt)
            if self.state_timer>0.5:
                self.state='idle'
                self.idle_timer=0.75+0.5*(random.random()**2)
                self.able_action=True
                self.frame=0
                self.state_timer=0
        elif self.state=='shoot':
            self.state_timer+=dt
            if self.state_timer<0.5:
                self.frame=(self.state_timer*6/0.5)%12
            elif self.state_timer<1:
                if not self.projflag:
                    self.projflag=True
                    tx,ty=play_loop.knight.x,play_loop.knight.y
                    tvx, tvy, temp1, tempdeg = self.facedirection(self.x, self.y, tx, ty)
                    spdmul=200
                    tvx *= spdmul
                    tvy *= spdmul
                    newproj=Slime_Projectile(self.x,self.y,tvx,tvy,4,500,False)
                    world.add_object(newproj,8)
                    self.proj.append(newproj)
                self.frame=(self.state_timer*6/0.5)%12
            else:
                self.frame=11
                self.state='idle'
                self.idle_timer=1.5
                self.able_action=True
                self.frame=0
                self.state_timer=0
        elif self.state=='death':
            play_loop.knight.money+=random.randint(7,15)
            self.delete=True
            # Slime_death
            pass
            #add more before and after...


        self.vbx,self.vby=self.vx,self.vy
        if self.vf:
            self.vx, self.vy = self.vbx,self.vby = self.vfx, self.vfy
            self.vf=False


        if not self.delete:
            world.collidecheck(self, "knight", "collidewithenemy")
            world.collidecheck(self, "monster", "collidewithteam")
        for case in self.collision:
            if case[0] in self.collisionchecked:
                pass
            else:
                if case[0].typename=="knight":
                    if self.state!="stagger" and self.state!="death" and self.state!="spawn" and self.state!="jump":
                        dirx, diry, _ = calculfuncs.facedircommon(self.x, self.y, case[0].x, case[0].y)
                        case[0].damageknockback(1,0, 200 * (dirx+4*self.vx), 200 * (diry+4*self.vy))
                        self.collisionchecked.append(case[0])
                elif case[0].typename=="monster":
                    #밀려날 때 예외처리
                    if self.height==0:
                        if self.x==case[0].x and self.y==case[0].y:
                            self.x+=random.random()-0.5
                            self.y+=random.random()-0.5
                        tempdist = math.sqrt((self.x - case[0].x) ** 2 + (self.y - case[0].y) ** 2)
                        if (self.x-case[0].x)**2+(self.y-case[0].y)**2 > (self.x+self.vbx-case[0].x-case[0].vbx)**2+(self.y+self.vby-case[0].y-case[0].vby)**2:
                            tmp_vx,tmp_vy=(self.vbx-case[0].vbx),(self.vby-case[0].vby)
                            if tmp_vx**2+tmp_vy**2>100:
                                self.vx/=math.sqrt(tmp_vx**2+tmp_vy**2)
                                self.vy/=math.sqrt(tmp_vx**2+tmp_vy**2)
                            self.vx-=tmp_vx/3
                            self.vy-=tmp_vy/3
                        self.collisionchecked.append(case[0])
            self.collision.remove(case)

        self.shadow.x,self.shadow.y=self.x,self.y

    def update_reverse(self):
        dt = play_loop.frame_time
        self.collisionchecked=[]

        if self.iframe>0:
            self.iframe-=dt
            if self.iframe<0:
                self.iframe=0

        for p in self.proj:
            if not p.hitanim:
                tx, ty = self.x, self.y
                tvx, tvy, temp1, tempdeg = self.facedirection(p.x, p.y, tx, ty)
                spdmul = 200
                tvx *= spdmul
                tvy *= spdmul
                p.vx, p.vy = tvx, tvy
                if (tx - p.x) ** 2 + (ty - p.y) ** 2 < (self.r + p.r) ** 2:
                    p.delete = True
                    self.proj.remove(p)
                    self.state_timer = 1.1
                    self.frame = 0
                    self.projflag = True
                    self.state = 'shoot'

        for a in self.areas:
            if a.life_timer>0:
                tx, ty = self.x, self.y
                tvx, tvy, temp1, tempdeg = self.facedirection(a.x, a.y, tx, ty)
                spdmul = 100
                tvx *= spdmul
                tvy *= spdmul
                a.x+=tvx*dt
                a.y+=tvy*dt
                if (tx - a.x) ** 2 + (ty - a.y) ** 2 < (self.r) ** 2:
                    a.life_timer=0.5
                elif a.life_timer<4.5:
                    a.life_timer+=1

        self.feedbackcheck()

        if self.state=='spawn':
            self.state='idle'
            self.state_timer=0
        elif self.state=='idle':
            tx,ty=play_loop.knight.x,play_loop.knight.y
            dist=math.sqrt((self.x-tx)**2+(self.y-ty)**2)
            if self.hp >= self.max_hp and random.random()>math.pow(0.9,dt):
                self.delete=True
                #Slime_spawn_reverse
            if self.rand_wait==0:
                self.idle_timer=0
                self.rand_wait_idle=1.25+0.5*(random.random()**2)
                self.rand_wait=random.random()*2
                if 200<=dist and self.rand_wait<=1.5:
                    self.state='teleport'
                    self.state_timer=0
                    return
                else:
                    self.rand_wait=self.rand_wait_idle
            self.idle_timer+=dt
            self.x+=self.vx
            self.y+=self.vy
            self.vx*=pow(0.05,dt)
            self.vy*=pow(0.05,dt)
            if self.idle_timer>=self.rand_wait_idle:
                if dist < SHOOT_DIST_MIN:
                    self.vx, self.vy, temp1, tempdeg = self.facedirection(self.x, self.y, tx, ty)
                    randegr = (random.random() - 0.5) * math.radians(60)
                    self.vx, self.vy, self.face_dir = self.degreeintofacedir(tempdeg + randegr)
                    dashdist = self.movespeed * (0.6 + (random.randint(0, 20) ** 2) * 0.001)
                    self.vx *= dashdist
                    self.vy *= dashdist
                    self.state = 'move'
                    self.state_timer = 0
                    self.rand_wait=0
                    self.frame = 0
                elif dist <= SHOOT_DIST_MAX:
                    if random.randint(0, 1):
                        self.vy, self.vx, temp1, tempdeg = self.facedirection(self.x, self.y, tx, ty)
                        randegr = (random.random() - 0.5) * math.radians(20)
                        self.vy, self.vx, self.face_dir = self.degreeintofacedir(tempdeg + randegr)
                        dashdist = self.movespeed * (0.6 + (random.randint(0, 20) ** 2) * 0.001)
                        self.vx *= dashdist
                        self.vy *= dashdist
                        self.state = 'move'
                        self.state_timer = 0
                        self.rand_wait=0
                        self.frame = 0
                    else:
                        self.state_timer = 1.1
                        self.frame = 0
                        self.projflag = False
                        self.rand_wait=0
                        self.state = 'shoot'
                elif dist <= 1000:
                    self.vx, self.vy, temp1, tempdeg = self.facedirection(tx, ty, self.x, self.y)
                    randegr = (random.random() - 0.5) * math.radians(60)
                    self.vx, self.vy, self.face_dir = self.degreeintofacedir(tempdeg + randegr)
                    dashdist = self.movespeed * (0.6 + (random.randint(0, 20) ** 2) * 0.001)
                    self.vx *= dashdist
                    self.vy *= dashdist
                    self.state = 'move'
                    self.state_timer = 0
                    self.rand_wait=0
                    self.frame = 0
                else:
                    randegr = (random.random() - 0.5) * math.radians(360)
                    self.vx, self.vy, self.face_dir = self.degreeintofacedir(randegr)
                    dashdist = self.movespeed * (0.3 + (random.randint(0, 20) ** 2) * 0.0005)
                    self.vx *= dashdist
                    self.vy *= dashdist
                    self.state = 'move'
                    self.state_timer = 0
                    self.rand_wait=0
                    self.frame = 0
        elif self.state=='stagger':
            self.state_timer+=dt
            self.x+=self.vx
            self.y+=self.vy
            self.vx*=pow(0.1,dt)
            self.vy*=pow(0.1,dt)
            if self.state_timer>FAINT_TIME:
                self.idle_timer=-0.3
                self.able_action=True
                self.state='idle'
        elif self.state=='move':
            self.state_timer-=dt
            self.frame=((0.5-self.state_timer)*4/0.4)
            if self.frame>3:self.frame=3
            self.x+=self.vx
            self.y+=self.vy
            self.vx*=pow(0.05,dt)
            self.vy*=pow(0.05,dt)
            if self.state_timer<=0:
                self.state='idle'
                self.idle_timer=-0.3
                self.able_action=True
                self.frame=0
                self.state_timer=0
        elif self.state=='shoot':
            self.state_timer-=dt
            if self.state_timer>1:
                if not self.projflag:
                    self.projflag=True
                    tx,ty=play_loop.knight.x,play_loop.knight.y
                    tvx, tvy, temp1, tempdeg = self.facedirection(self.x, self.y, tx, ty)
                    distmul=500
                    tvx *= distmul
                    tvy *= distmul
                    newarea=Area(self.x+tvx,self.y+tvy,64,5.0,0,1,True,0,["knight"])
                    world.add_object(newarea,6)
                    self.areas.append(newarea)
                    newproj=Slime_Projectile(self.x+tvx,self.y+tvy,1,1,4,500,True)
                    world.add_object(newproj,8)
                    self.proj.append(newproj)
                self.state_timer=1.0
            elif self.state_timer>0.5:
                self.frame=(self.state_timer*6/0.5)%12
            elif self.state_timer>0:
                self.frame=(self.state_timer*6/0.5)%12
                pass
            else:
                self.state='idle'
                self.idle_timer=-0.3
                self.able_action=True
                self.frame=0
                self.state_timer=0

        elif self.state=='teleport':
            if self.state_timer==0:
                tx,ty=play_loop.knight.x,play_loop.knight.y
                dist=math.sqrt((self.x-tx)**2+(self.y-ty)**2)
                tmp_vx, tmp_vy, temp1, tempdeg = self.facedirection(self.x, self.y, tx, ty)
                randegr = (random.random() - 0.5) * math.radians(60)
                tmp_vx, tmp_vy, self.face_dir = self.degreeintofacedir(tempdeg + randegr)
                self.x+=(random.randint(25, max(100,min(int(dist-200),400))))*tmp_vx
                self.y+=(random.randint(25, max(100,min(int(dist-200),400))))*tmp_vy
            self.state_timer+=dt
            tx,ty=play_loop.knight.x,play_loop.knight.y
            dist=math.sqrt((self.x-tx)**2+(self.y-ty)**2)
            if self.state_timer<0.25:
                self.frame=(self.frame+dt/0.05)%4
            else:
                self.frame=4+(self.frame+dt/0.05)%2
            if self.state_timer>0.3:
                if dist>200 and random.random()<0.8:
                    self.state_timer=0
                else:
                    self.state='idle'
                    self.state_timer=0
                    self.frame=0
        elif self.state=='spawn':
            self.delete=True
            pass
            #add more before and after...

        self.vbx, self.vby = self.vx, self.vy
        if self.vf:
            self.vx, self.vy = self.vbx,self.vby = self.vfx, self.vfy
            self.vf=False

        world.collidecheck(self,"knight","collidewithenemy")
        world.collidecheck(self,"monster","collidewithteam")
        for case in self.collision:
            if case[0] in self.collisionchecked:
                pass
            else:
                if case[0].typename=="knight":
                    if self.state!="stagger" and self.state!="death" and self.state!="spawn" and self.state!="jump":
                        dirx, diry, _ = calculfuncs.facedircommon(self.x, self.y, case[0].x, case[0].y)
                        case[0].damageknockback(1,0, 200 * (dirx+4*self.vx), 200 * (diry+4*self.vy))
                        self.collisionchecked.append(case[0])
                elif case[0].typename=="monster":
                    #밀려날 때 예외처리
                    if self.height==0:
                        if self.x==case[0].x and self.y==case[0].y:
                            self.x+=random.random()-0.5
                            self.y+=random.random()-0.5
                        tempdist = math.sqrt((self.x - case[0].x) ** 2 + (self.y - case[0].y) ** 2)
                        if (self.x-case[0].x)**2+(self.y-case[0].y)**2 > (self.x+self.vbx-case[0].x-case[0].vbx)**2+(self.y+self.vby-case[0].y-case[0].vby)**2:
                            tmp_vx,tmp_vy=(self.vbx-case[0].vbx),(self.vby-case[0].vby)
                            if tmp_vx**2+tmp_vy**2>100:
                                self.vx/=math.sqrt(tmp_vx**2+tmp_vy**2)
                                self.vy/=math.sqrt(tmp_vx**2+tmp_vy**2)
                            self.vx-=tmp_vx/0.9
                            self.vy-=tmp_vy/0.9
                        self.collisionchecked.append(case[0])
                        pass
            self.collision.remove(case)

        self.shadow.x,self.shadow.y=self.x,self.y

    def onhit(self,ax,ay):
        pass

    def deleteaction(self):
        for area in self.areas:
            area.delete=True
        for p in self.proj:
            if self. reverse:
                p.delete=True
                if p.shadow!=None:
                    p.shadow.delete=True
            else:
                p.noowner=True
        if not self.shadow==None:
            self.shadow.delete=True

    def draw(self):
        if self.state=='idle' or self.state=="stagger":
            Shooter_Slime.move_image.clip_draw(96, 0, 32, 32,int((self.x - play_loop.cam_x) / 2) * 2,int((self.y - play_loop.cam_y) / 2) * 2 + 8, 64,64)
        elif self.state=='move':
            Shooter_Slime.move_image.clip_draw((int(self.frame) % 4) * 32, self.face_dir * 32, 32, 32,int((self.x - play_loop.cam_x) / 2) * 2,int((self.y - play_loop.cam_y) / 2) * 2 + 8, 64, 64)
        elif self.state=='shoot':
            Shooter_Slime.shoot_image.clip_draw(int(self.frame%3)*32,int(4-((self.frame)/3)) * 32, 32, 32,int((self.x - play_loop.cam_x) / 2) * 2,int((self.y+self.height - play_loop.cam_y) / 2) * 2 + 8, 64, 64)
        elif self.state=='teleport':
            Shooter_Slime.teleport_image.clip_draw(0,int(self.frame) * 32, 32, 32,int((self.x - play_loop.cam_x) / 2) * 2,int((self.y - play_loop.cam_y) / 2) * 2 + 8, 64, 64)

class Slime_Projectile:
        image = None

        def __init__(self,x,y,vx,vy,r=4,range=0,reversed=False):
            if Slime_Projectile.image==None:
                Slime_Projectile.image=load_image("slimeproj.png")
            self.x,self.y = x,y
            self.vx,self.vy=vx,vy
            self.r=r
            self.air_max_timer = range/math.sqrt(self.vx**2+self.vy**2)
            self.frame = 0
            self.typename = "projectile"
            self.noowner=False
            self.delete = False
            self.deleteready=False
            self.spawnanim=False
            self.reverse=reversed
            self.hitanim = self.reverse
            self.area=[]
            self.collision=[]
            self.collisionchecked = []
            if self.reverse:
                self.shadow=None
                self.air_timer=-0.3
            else:
                self.shadow=Shadow(self.x,self.y,0)
                world.add_object(self.shadow,5)
                self.air_timer=self.air_max_timer

        def update(self):
            if self.reverse:
                self.update_reverse()
            else:
                self.update_normal()

        def update_normal(self):
            self.collisionchecked = []
            dt = play_loop.frame_time
            self.air_timer -= dt
            if self.hitanim:
                if self.shadow!=None:
                    world.remove_object(self.shadow)
                    self.shadow = None
                if self.air_timer < -0.3:
                    if self.noowner:
                        self.delete=True
                    else:
                        self.deleteready=True
                else:
                    self.frame=1+(self.air_timer*8/-0.3)
                pass
            else:
                self.x += self.vx * dt
                self.y += self.vy * dt
                if self.air_timer < 0:
                    self.hitanim=True
                self.shadow.x,self.shadow.y=self.x,self.y

            world.collidecheck(self, "knight", "collidewithenemy")
            for case in self.collision:
                if case[0] in self.collisionchecked:
                    pass
                else:
                    if case[0].typename == "knight":
                        if not self.hitanim:
                            dirx, diry, _ = calculfuncs.facedircommon(self.x, self.y, case[0].x, case[0].y)
                            case[0].damageknockback(1, 0, 1 * (dirx + 4 * self.vx), 1 * (diry + 4 * self.vy))
                            self.hitanim=True
                            self.air_timer=0
                self.collision.remove(case)

        def update_reverse(self):
            self.collisionchecked = []
            dt = play_loop.frame_time
            self.air_timer += dt
            if self.hitanim:
                if self.air_timer > 0:
                    self.hitanim = False
                    self.shadow = Shadow(self.x, self.y, 0)
                    world.add_object(self.shadow, 5)
                else:
                    self.frame = 1 + (self.air_timer * 8 / -0.3)
                pass
            else:
                self.frame = 0
                self.x += self.vx * dt
                self.y += self.vy * dt
                if self.shadow!=None:
                    self.shadow.x, self.shadow.y = self.x, self.y
            world.collidecheck(self, "knight", "collidewithenemy")
            for case in self.collision:
                if case[0] in self.collisionchecked:
                    pass
                else:
                    if case[0].typename == "knight":
                        if not self.hitanim:
                            dirx, diry, _ = calculfuncs.facedircommon(self.x, self.y, case[0].x, case[0].y)
                            case[0].damageknockback(1, 1, 1 * (dirx + 4 * self.vx), 1 * (diry + 4 * self.vy))
                            self.deleteready=True
                self.collision.remove(case)

        def draw(self):
                if self.hitanim:
                    Slime_Projectile.image.clip_draw(16*int(self.frame)%3, 16*int((8-self.frame)/3), 16, 16, int((self.x - play_loop.cam_x) / 2) * 2,
                                               int((self.y - play_loop.cam_y) / 2) * 2, 32, 32)
                else:
                    Slime_Projectile.image.clip_draw(16*int(self.frame)%3, 16*int((8-self.frame)/3), 16, 16, int((self.x - play_loop.cam_x) / 2) * 2,
                                               int((self.y - play_loop.cam_y) / 2) * 2 + 12, 32, 32)
        def deleteaction(self):
            for a in self.area:
                a.life_timer=0.0
            if self.shadow!=None:
                self.shadow.delete=True
                self.shadow=None