from pico2d import load_image, get_time, load_font, draw_rectangle,clamp
import math
import calculfuncs
import play_loop
import random

from sdl2 import SDL_HINT_WINDOWS_NO_CLOSE_ON_ALT_F4

import play_loop
import world
from ui import Popup,addpopup

class Interactobj:
    obj_image=None
    warp_image=None
    def __init__(self,x=1200,y=300,r=32,pw=64,ph=64,pr=100,reverse=False,imagetype=0,price=[],give=[],text=[]):
        self.images()
        self.reverse=reverse
        self.anim_timer=-0.5
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
        self.typename="interact"
        self.delete=False
        self.areatoggle=False
        if self.imagetype==0:
            self.frame=4
        elif self.imagetype==1:
            self.frame=9
        elif self.imagetype==2:
            self.frame=10
        elif self.imagetype==3:
            self.frame=0
        elif self.imagetype==4:
            self.frame=0
        elif self.imagetype==5:
            self.frame=1
        else:
            self.frame=1

    def images(self):
        if Interactobj.obj_image is None:
            Interactobj.obj_image=load_image('shopobj.png')
        if Interactobj.warp_image is None:
            Interactobj.warp_image=load_image('warpthing.png')

    def update(self):
        dt = play_loop.frame_time
        if self.anim_timer>=0:
            self.anim_timer += dt
            self.frame = int(self.anim_timer*8)
            if int(self.anim_timer*8)>5:
                self.anim_timer=1
                self.delete=True
        dist_pow=(play_loop.knight.x-self.x)**2+(play_loop.knight.y-self.y)**2

        priceflag = True
        for thing in self.price:
            if thing[0] == 'money':
                if play_loop.knight.money < thing[1]:
                    priceflag = False
        if priceflag and dist_pow<=self.popup_r**2 and self.text!=[]:
            if self.imagetype == 0:
                self.frame = 5
            elif self.imagetype == 1:
                self.frame = 6
            elif self.imagetype == 2:
                self.frame = 11
            elif self.imagetype == 3:
                pass
            else:
                pass
        else:
            if self.imagetype == 0:
                self.frame = 4
            elif self.imagetype == 1:
                self.frame = 9
            elif self.imagetype == 2:
                self.frame = 10
            elif self.imagetype == 3:
                pass
            else:
                pass
        if dist_pow<=self.popup_r**2 and self.text!=[]:
            if not self.areatoggle:
                self.areatoggle=True

                if len(self.popup) == 0:
                    added_popup = Popup(self.x, self.y + 50, 0, 0, self.popup_w, self.popup_h, self.text)
                    self.popup.append(added_popup)
                    addpopup(added_popup)
                else:
                    self.popup[0].tw, self.popup[0].th = self.popup_w, self.popup_h
        else:
            if self.areatoggle:
                self.areatoggle=False
                if self.imagetype == 0:
                    self.frame = 4
                elif self.imagetype == 1:
                    self.frame = 9
                elif self.imagetype == 2:
                    self.frame = 10
                elif self.imagetype == 3:
                    pass
                else:
                    pass
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
                        for thing in self.price:
                            if thing[0] == 'money':
                                case[0].money-=thing[1]
                        for thing in self.give:
                            if thing[0]=='max_hp':
                                case[0].max_hp+=thing[1]
                            elif thing[0]=='max_paradox':
                                case[0].max_paradox+=thing[1]
                            elif thing[0]=='attackdamage':
                                case[0].attackdamage+=thing[1]
                            elif thing[0]=='walk_speed':
                                case[0].walkspeed+=thing[1]
                            elif thing[0]=='attack_speed':
                                case[0].attackspeed+=thing[1]
                            elif thing[0]=='attack_charge':
                                case[0].attackchargetime+=thing[1]
                            elif thing[0]=='attack_range':
                                case[0].attackrange+=thing[1]
                            elif thing[0]=='trigger_wave':
                                self.anim_timer=dt
                                play_loop.knight.hp+=2
                                if play_loop.knight.hp>play_loop.knight.max_hp:
                                    play_loop.knight.hp=play_loop.knight.max_hp
                                if play_loop.knight.paradox>0:
                                    play_loop.knight.paradox = int((play_loop.knight.paradox-1)/3)*3
                                #???
                        self.price=[]
                        self.give=[]
                        self.text=[]
                    pass

            self.collision.remove(case)

    def draw(self):
        if self.imagetype==3:
            Interactobj.warp_image.clip_draw(0, int(4-self.frame) * 64, 64, 64,int((self.x - play_loop.cam_x) / 2) * 2,int((self.y - play_loop.cam_y) / 2) * 2, 128, 128)
        else:
            Interactobj.obj_image.clip_draw(int(self.frame%2) *64,int(self.frame/2)*64, 64, 64, int((self.x - play_loop.cam_x) / 2) * 2,int((self.y - play_loop.cam_y) / 2) * 2, 128, 128)

    def sendfeedback(self,fdbk):
        self.feedback.append(fdbk)

    def deleteaction(self):
        if self.imagetype==3:
            play_loop.start_wave(0, 0, 32)
        for pop in self.popup:
            pop.tw,pop.th=-1,-1
            pop.autodelete=True
        self.popup=[]
        pass

def setshop_armor(x,y):
    text=[]
    cost=[]
    give=[]
    raffle=[]
    raffle.append("armor_hp")#max_hp+???
    if play_loop.knight.max_hp>2:
        raffle.append("armor_para")    #max_hp-2,max_para+3
    seted=raffle.pop(random.randint(0,len(raffle)-1))
    if seted=="armor_hp":
        stat=random.randint(1,int(play_loop.knight.max_hp/10+1))*2
        price=int(stat)*int(play_loop.knight.max_hp)*random.randint(2,5)
        give.append(["max_hp",stat])
        text.append("H+"+str(int(stat/2)))
        text.append(str(price)+"G")
        cost.append(["money",price])
        newobj=Interactobj(x,y,r=8,pw=48,ph=32,pr=150,imagetype=0,price=cost,give=give,text=text)
    elif seted=="armor_para":
        price=3*random.randint(30,60)
        text.append("H-1")
        text.append("P+1")
        text.append(str(price)+"G")
        cost.append(["money",price])
        give.append(["max_hp",-2])
        give.append(["max_paradox",3])
        newobj=Interactobj(x,y,r=8,pw=48,ph=32,pr=150,imagetype=0,price=cost,give=give,text=text)
    world.add_object(newobj,8)

def setshop_sword(x, y):
    text = []
    cost = []
    give = []
    stat=random.randint(1,int(1+play_loop.knight.attackdamage/5))
    price=stat*random.randint(30,60)
    text.append("A+"+str(stat))
    text.append(str(price)+"G")
    cost.append(["money",price])
    give.append(["attackdamage",stat])
    newobj=Interactobj(x,y,r=8,pw=48,ph=32,pr=150,imagetype=1,price=cost,give=give,text=text)
    world.add_object(newobj,8)
    # atk+???

def setshop_potions(x, y):
    text = []
    cost = []
    give = []
    raffle=[]
    price=random.randint(50,200)
    raffle.append("walk_speed")
    raffle.append("attack_speed")
    raffle.append("attack_charge")
    raffle.append("attack_range")
    # random_stat_increase+3
    text.append("???")
    text.append(str(price)+"G")
    cost.append(["money",price])
    seted=raffle.pop(random.randint(0,len(raffle)-1))
    if seted=="walk_speed":
        give.append(["walk_speed",random.randint(1,40)])
    elif seted=="attack_speed":
        give.append(["attack_speed",random.randint(10,400)])
    elif seted=="attack_charge":
        give.append(["attack_charge",-random.random()*0.1*play_loop.knight.attackchargetime])
    elif seted=="attack_range":
        give.append(["attack_range",random.randint(1,30)])
    newobj = Interactobj(x, y, r=8, pw=48, ph=32, pr=150, imagetype=2, price=cost, give=give, text=text)
    world.add_object(newobj, 8)



