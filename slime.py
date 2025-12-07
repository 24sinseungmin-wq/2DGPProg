from pico2d import load_image, get_time, load_font, draw_rectangle,clamp
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
MAX_HEIGHT=600
#MAX_KB_SPEED=20
JUMP_DIST_MAX=500
JUMP_DIST_MIN=200
EXTRA_PARADOX_TIME=1.5

class Slime(Monster):
    jump_image=None
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

        self.shadow=None
        self.shadow=Shadow(self.x,self.y,0)
        world.add_object(self.shadow,5)

    def images(self):
        if Slime.jump_image==None:
            Slime.jump_image=load_image('slime_jump.png')
        if Slime.move_image==None:
            Slime.move_image=load_image('slime_move.png')
        if Slime.teleport_image==None:
            Slime.teleport_image=load_image('slime_teleport.png')
        #Slime.hit_image

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

        if self.iframe>0:
            self.iframe-=dt
            if self.iframe<0:
                self.iframe=0
        if self.state=='spawn':
            self.state='idle'
            self.state_timer=0
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
                if dist>300 and dist<500 and random.random()>0.2:
                    self.state='jump'   #일정 확률로 점프 시도하도록 변경?
                    self.state_timer=0
                    self.frame=0
                elif dist<500 or dist<(random.random())*1000:
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
                pass
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
                self.idle_timer=0.5+0.5*(random.random()**2)
                self.able_action=True
                self.frame=0
                self.state_timer=0
        elif self.state=='jump':
            self.state_timer+=dt
            if self.state_timer<=0.15:
                self.frame=(self.state_timer*3/0.15)
                self.x+=self.vx*dt
                self.y+=self.vy*dt
                self.vx*=pow(0.01,dt)
                self.vy*=pow(0.01,dt)
                self.sx,self.sy=self.x,self.y
                self.tx,self.ty=play_loop.knight.x,play_loop.knight.y
                if math.sqrt((self.sx-self.tx)**2+(self.sy-self.ty)**2)>JUMP_DIST_MAX:
                    regu=JUMP_DIST_MAX/math.sqrt((self.sx-self.tx)**2+(self.sy-self.ty)**2)
                    self.tx -= self.sx
                    self.ty -= self.sy
                    self.tx *= regu
                    self.ty *= regu
                    self.tx += self.sx
                    self.ty += self.sy
            elif self.state_timer<=0.25:
                if self.height==0:
                    self.sx, self.sy = self.x, self.y
                    self.tx, self.ty = play_loop.knight.x, play_loop.knight.y
                    tempvx,tempvy,temp1=self.degreeintofacedir(random.random()*2*math.pi)
                    if math.sqrt((self.sx-self.tx)**2+(self.sy-self.ty)**2)>JUMP_DIST_MAX:
                        regu=JUMP_DIST_MAX/math.sqrt((self.sx-self.tx)**2+(self.sy-self.ty)**2)
                        self.tx -= self.sx
                        self.ty -= self.sy
                        self.tx *= regu
                        self.ty *= regu
                        self.tx += self.sx
                        self.ty += self.sy
                    self.tx += 60 * tempvx * random.random()**2
                    self.ty += 60 * tempvy * random.random()**2
                    self.tx = clamp(self.r-play_loop.background.w / 4, self.tx, play_loop.background.w / 4-self.r)
                    self.ty = clamp(self.r-play_loop.background.h / 4, self.ty, play_loop.background.h / 4-self.r)
                    area=Area(self.tx,self.ty,32,1.25-self.state_timer,2,0,False,300,["knight"])
                    world.add_object(area,6)
                    self.areas.append(area)
                t=0.5*(1+math.sin(((self.state_timer-0.15)/1.2-0.5)*math.pi))
                self.x=self.tx*(t)+self.sx*(1-t)
                self.y=self.ty*(t)+self.sy*(1-t)
                self.height=MAX_HEIGHT*(1-((self.state_timer-0.15)/0.6-1)**2)
            elif self.state_timer<1.25:
                self.height=MAX_HEIGHT*(1-((self.state_timer-0.15)/0.6-1)**2)
                self.frame=3
                t=0.5*(1+math.sin(((self.state_timer-0.15)/1.2-0.5)*math.pi))
                self.x=self.tx*(t)+self.sx*(1-t)
                self.y=self.ty*(t)+self.sy*(1-t)
            elif self.state_timer<=1.35:
                t=0.5*(1+math.sin(((self.state_timer-0.15)/1.2-0.5)*math.pi))
                self.x=self.tx*(t)+self.sx*(1-t)
                self.y=self.ty*(t)+self.sy*(1-t)
                self.height=MAX_HEIGHT*(1-((self.state_timer-0.15)/0.6-1)**2)
                self.frame=3
                self.x+=self.vx*dt
                self.y+=self.vy*dt
                self.vx*=pow(0.01,dt)
                self.vy*=pow(0.01,dt)
            elif self.state_timer<1.5:
                self.height=0
                self.frame=4+((self.state_timer-1.35)*5/0.15)
                self.x+=self.vx*dt
                self.y+=self.vy*dt
                self.vx*=pow(0.01,dt)
                self.vy*=pow(0.01,dt)
            else:
                self.state='idle'
                self.idle_timer=1.5
                self.able_action=True
                self.frame=0
                self.state_timer=0
        elif self.state=='death':
            play_loop.knight.money+=random.randint(10,25)
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

        self.feedbackcheck()

        if self.state=='spawn':
            self.state='idle'
            self.state_timer=0
        elif self.state=='idle':
            tx,ty=play_loop.knight.x,play_loop.knight.y
            dist=math.sqrt((self.x-tx)**2+(self.y-ty)**2)
            if self.hp >= self.max_hp and random.random()>math.pow(0.5,dt):
                self.delete=True
                play_loop.knight.money += random.randint(50, 100)
                #Slime_spawn_reverse
            elif self.rand_wait==0:
                self.idle_timer=0
                self.rand_wait_idle=0.5+0.5*(random.random()**2)
                self.rand_wait=random.random()*3
                if 50<=dist and self.rand_wait<=0.75:
                    self.state='teleport'
                    self.state_timer=0
                    return
                elif dist < min(250+random.random()*150,play_loop.knight.walkspeed*2) and self.rand_wait>=1.5 and play_loop.knight.parapos_check(self.x,self.y,self.r+64):
                    self.rand_wait=1.51
                    play_loop.knight.set_parapos(self.x,self.y,64)
                else:
                    self.rand_wait=self.rand_wait_idle
            self.idle_timer+=dt
            self.x+=self.vx
            self.y+=self.vy
            self.vx*=pow(0.05,dt)
            self.vy*=pow(0.05,dt)
            if self.idle_timer>=self.rand_wait:
                if self.rand_wait >= 1.0:
                    self.state = 'jump'
                    self.hpareaflag = True
                    self.state_timer = 1.6
                    self.frame = 0
                    self.rand_wait=0
                elif self.idle_timer>=self.rand_wait_idle:
                    if dist < 450 or dist < random.random() * 1000:
                        self.vx, self.vy, temp1, tempdeg = self.facedirection(self.x, self.y, tx, ty)
                        randegr = (random.random() - 0.5) * math.radians(60)
                        self.vx, self.vy, self.face_dir = self.degreeintofacedir(tempdeg + randegr)
                        dashdist = self.movespeed * (0.6 + (random.randint(0, 20) ** 2) * 0.001)
                    else:
                        randegr = (random.random() - 0.5) * math.radians(360)
                        self.vx, self.vy, self.face_dir = self.degreeintofacedir(randegr)
                        dashdist = self.movespeed * (0.3 + (random.randint(0, 20) ** 2) * 0.0005)
                    self.vx *= -dashdist
                    self.vy *= -dashdist
                    self.state = 'move'
                    self.state_timer = 0.5
                    self.frame = 0
                    self.rand_wait=0
            elif self.rand_wait>=2.0 and (not play_loop.knight.parapos_check(self.x, self.y, self.r + 64) or dist > max(play_loop.knight.walkspeed*2.5,400)):
                self.rand_wait=self.rand_wait_idle
        elif self.state=='stagger':
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
            self.state_timer-=dt
            self.frame=((0.5-self.state_timer)*4/0.4)
            if self.frame>3:self.frame=3
            self.x+=self.vx
            self.y+=self.vy
            self.vx*=pow(0.05,dt)
            self.vy*=pow(0.05,dt)
            if self.state_timer<=0:
                self.state='idle'
                self.idle_timer=0
                self.able_action=True
                self.frame=0
                self.state_timer=0
        elif self.state=='jump':
            self.state_timer-=dt
            if self.state_timer<=0:
                self.state='idle'
                self.state_timer=0
                self.idle_timer=0
                self.frame=0
            elif self.state_timer<0.15:
                self.height=0
                self.frame=(self.state_timer*4/0.15)
            elif self.state_timer<0.25:
                self.x+=self.vx*dt
                self.y+=self.vy*dt
                self.vx*=pow(0.01,dt)
                self.vy*=pow(0.01,dt)
                self.frame = 3
                t=0.5*(1+math.sin(((self.state_timer-0.15)/1.2-0.5)*math.pi))
                self.x=self.tx*(1-t)+self.sx*(t)
                self.y=self.ty*(1-t)+self.sy*(t)
                self.height=MAX_HEIGHT*(1-((self.state_timer-0.15)/0.6-1)**2)
            elif self.state_timer<0.35:
                self.frame = 3
                self.height=MAX_HEIGHT*(1-((self.state_timer-0.15)/0.6-1)**2)
                t=0.5*(1+math.sin(((self.state_timer-0.15)/1.2-0.5)*math.pi))
                self.x=self.tx*(1-t)+self.sx*(t)
                self.y=self.ty*(1-t)+self.sy*(t)
            elif self.state_timer<1.35:
                if self.height==0:
                    self.sx, self.sy = self.x, self.y
                    tx, ty = play_loop.knight.x, play_loop.knight.y
                    tmp_vx, tmp_vy, temp1, tempdeg = self.facedirection(self.x, self.y, tx, ty)
                    randegr = tempdeg+((random.random() - 0.5)**2) * math.radians(120)
                    tmp_vx, tmp_vy, self.face_dir = self.degreeintofacedir(randegr)
                    jumpdist=JUMP_DIST_MIN+(random.random()**2)*(JUMP_DIST_MAX-JUMP_DIST_MIN)
                    tmp_vx*=-jumpdist
                    tmp_vy*=-jumpdist
                    self.tx,self.ty=tmp_vx+self.x,tmp_vy+self.y
                    self.tx = clamp(self.r-play_loop.background.w / 4, self.tx, play_loop.background.w / 4-self.r)
                    self.ty = clamp(self.r-play_loop.background.h / 4, self.ty, play_loop.background.h / 4-self.r)
                    area = Area(self.x, self.y, 64, self.state_timer+EXTRA_PARADOX_TIME, 0, 2, False, 0, ["knight"])
                    world.add_object(area, 6)
                    self.areas.append(area)
                t=0.5*(1+math.sin(((self.state_timer-0.15)/1.2-0.5)*math.pi))
                self.x=self.tx*(1-t)+self.sx*(t)
                self.y=self.ty*(1-t)+self.sy*(t)
                self.height=MAX_HEIGHT*(1-((self.state_timer-0.15)/0.6-1)**2)
                self.frame=3
                self.x+=self.vx*dt
                self.y+=self.vy*dt
                self.vx*=pow(0.01,dt)
                self.vy*=pow(0.01,dt)
            elif self.state_timer<1.5:
                if self.hpareaflag:
                    area=Area(self.x,self.y,32,0.25,2,0,True,-300,["knight"])
                    world.add_object(area,6)
                    self.areas.append(area)
                    self.hpareaflag=False
                self.height=0
                self.frame=4+((self.state_timer-1.35)*5/0.15)
                if self.frame>9:
                    self.frame=9
                self.x+=self.vx*dt
                self.y+=self.vy*dt
                self.vx*=pow(0.01,dt)
                self.vy*=pow(0.01,dt)
            else:
                self.able_action=False
        elif self.state=='teleport':
            if self.state_timer==0:
                tx,ty=play_loop.knight.x,play_loop.knight.y
                dist=math.sqrt((self.x-tx)**2+(self.y-ty)**2)
                tmp_vx, tmp_vy, temp1, tempdeg = self.facedirection(self.x, self.y, tx, ty)
                randegr = (random.random() - 0.5) * math.radians(60)
                tmp_vx, tmp_vy, self.face_dir = self.degreeintofacedir(tempdeg + randegr)
                self.x+=(random.randint(25,min(int(dist-25),400)))*tmp_vx
                self.y+=(random.randint(25,min(int(dist-25),400)))*tmp_vy
            self.state_timer+=dt
            tx,ty=play_loop.knight.x,play_loop.knight.y
            dist=math.sqrt((self.x-tx)**2+(self.y-ty)**2)
            if self.state_timer<0.25:
                self.frame=(self.frame+dt/0.05)%4
            else:
                self.frame=4+(self.frame+dt/0.05)%2
            if self.state_timer>0.3:
                if dist>250 and random.random()<0.8:
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
        if not self.shadow==None:
            self.shadow.delete=True

    def draw(self):
        if self.state=='idle' or self.state=="stagger":
            Slime.jump_image.clip_draw(0, 0, 32, 32,int((self.x - play_loop.cam_x) / 2) * 2,int((self.y - play_loop.cam_y) / 2) * 2 + 8, 64,64)
        elif self.state=='move':
            Slime.move_image.clip_draw((int(self.frame) % 4) * 32, self.face_dir * 32, 32, 32,int((self.x - play_loop.cam_x) / 2) * 2,int((self.y - play_loop.cam_y) / 2) * 2 + 8, 64, 64)
        elif self.state=='jump':
            Slime.jump_image.clip_draw(0,int(9-self.frame) * 32, 32, 32,int((self.x - play_loop.cam_x) / 2) * 2,int((self.y+self.height - play_loop.cam_y) / 2) * 2 + 8, 64, 64)
        elif self.state=='teleport':
            Slime.teleport_image.clip_draw(0,int(self.frame) * 32, 32, 32,int((self.x - play_loop.cam_x) / 2) * 2,int((self.y - play_loop.cam_y) / 2) * 2 + 8, 64, 64)
