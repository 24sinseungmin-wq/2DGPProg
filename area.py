from pico2d import load_image, get_time, load_font, draw_rectangle,clamp
import math
import calculfuncs

from sdl2 import SDL_HINT_WINDOWS_NO_CLOSE_ON_ALT_F4

import play_loop
import world

SMALL_R=16
LARGE_R=32
HP_DMG_DEFAULT_DESPAWN_TIME=0.3
HP_PARADOX_DEFAULT_DEACTIVATE_TIME=0.2
HP_PARADOX_DEFAULT_ACTIVATE_TIME=0.3

class Area:
    damage_hp_area_image = None
    damage_paradox_area_image = None
    def __init__(self,x=1200,y=300,r=32,life_timer=1.0,dmg=0,paradox=0,reverse=False,knockback=0,damageto=["knight"]):
        self.images()
        self.reverse=reverse
        self.life_timer = self.max_life_timer=life_timer
        self.blink_timer=0
        self.special_action_timer=HP_DMG_DEFAULT_DESPAWN_TIME
        self.special_action = None
        self.frame=0
        self.x=x
        self.y=y
        self.knockback=knockback
        self.r=r
        self.feedback=[]
        self.collision=[]
        self.collisionchecked=[]
        self.typename="area"
        self.hp_dmg=dmg
        self.paradox_dmg=paradox
        self.delete=False
        self.damageto=damageto
        self.areas=[]

    def images(self):
        if Area.damage_hp_area_image==None:
            Area.damage_hp_area_image=load_image('damage_area.png')
        if Area.damage_paradox_area_image==None:
            Area.damage_paradox_area_image=load_image('paradox_area.png')

    def update(self):
        if self.reverse:
            self.update_reverse()
        else:
            self.update_normal()

    def update_normal(self):
        dt = play_loop.frame_time
        if self.hp_dmg != 0:
            if self.special_action != 'despawn':
                self.life_timer -= dt
                if self.life_timer <= 0:
                    self.special_action = 'despawn'
                    self.special_action_timer = HP_DMG_DEFAULT_DESPAWN_TIME
                else:
                    blink_speed = clamp(0.03, 0.02 + self.life_timer / 10, 0.5)
                    if self.blink_timer <= 0:
                        self.frame = 0
                        self.blink_timer = 1 + 0.1 / blink_speed
                    else:
                        self.blink_timer -= dt / blink_speed
                        if self.blink_timer > 1:
                            self.frame = 0
                        else:
                            self.frame = 1
            else:
                self.special_action_timer -= dt
                self.frame = 2 + ((HP_DMG_DEFAULT_DESPAWN_TIME - self.special_action_timer) / HP_DMG_DEFAULT_DESPAWN_TIME * 7) % 7
                if self.special_action_timer <= 0:
                    self.delete = True
            pass
        elif self.hp_dmg == 0 and self.paradox_dmg > 0:
            if self.special_action == None:
                self.life_timer -= dt
                if self.life_timer <= 0:
                    self.special_action = 'activate'
                    self.special_action_timer = HP_PARADOX_DEFAULT_ACTIVATE_TIME
                    play_loop.knight.damage_ignore_iframe(self.paradox_dmg)
                else:
                    blink_speed = clamp(0.03, 0.02 + self.life_timer / 10, 0.5)
                    if self.blink_timer <= 0:
                        self.frame = 0
                        self.blink_timer = 1 + 0.1 / blink_speed
                    else:
                        self.blink_timer -= dt / blink_speed
                        if self.blink_timer > 1:
                            self.frame = 0
                        else:
                            self.frame = 1
            elif self.special_action == 'deactivate':
                self.special_action_timer -= dt
                self.frame = 4 + ((HP_PARADOX_DEFAULT_DEACTIVATE_TIME - self.special_action_timer) / HP_PARADOX_DEFAULT_DEACTIVATE_TIME * 4) % 4
                if self.special_action_timer <= 0:
                    self.delete = True
            else:
                self.special_action_timer -= dt
                self.frame = 8 + ((HP_PARADOX_DEFAULT_ACTIVATE_TIME - self.special_action_timer) / HP_PARADOX_DEFAULT_ACTIVATE_TIME * 8) % 8
                if self.special_action_timer <= 0:
                    self.delete = True

        if not self.delete:
            world.collidecheck(self, "knight", "knightinarea")
            world.collidecheck(self, "monster", "monsterinarea")

        for case in self.collision:
            if case[0] in self.collisionchecked:
                pass
            else:
                if case[0].typename == "knight":
                    if self.hp_dmg == 0 and self.paradox_dmg>0 and self.life_timer > 0 and self.special_action!='deactivate':
                        if "knight" in self.damageto:
                            self.special_action = 'deactivate'
                            self.special_action_timer = HP_PARADOX_DEFAULT_DEACTIVATE_TIME
                    elif self.hp_dmg>0 and self.life_timer <= 0:
                        if "knight" in self.damageto:
                            dirx, diry, _ = calculfuncs.facedircommon(self.x, self.y, case[0].x, case[0].y)
                            case[0].damageknockback(self.hp_dmg, self.paradox_dmg, self.knockback*dirx, self.knockback*diry)
                            self.collisionchecked.append(case[0])
            self.collision.remove(case)

    def update_reverse(self):
        dt = play_loop.frame_time
        if self.hp_dmg != 0 and self.r < 48:
            if self.special_action != 'despawn':
                self.life_timer -= dt
                if self.life_timer <= 0:
                    self.special_action = 'despawn'
                    self.special_action_timer = HP_DMG_DEFAULT_DESPAWN_TIME
                else:
                    blink_speed = clamp(0.03, 0.02 + self.life_timer / 10, 0.5)
                    if self.blink_timer <= 0:
                        self.frame = 0
                        self.blink_timer = 1 + 0.1 / blink_speed
                    else:
                        self.blink_timer -= dt / blink_speed
                        if self.blink_timer > 1:
                            self.frame = 0
                        else:
                            self.frame = 1
            else:
                self.special_action_timer -= dt
                self.frame = 2 + (
                        7 - ((HP_DMG_DEFAULT_DESPAWN_TIME - self.special_action_timer) / HP_DMG_DEFAULT_DESPAWN_TIME * 7) % 7)
                if self.special_action_timer <= 0:
                    self.delete = True
            pass
        elif self.hp_dmg == 0 and self.paradox_dmg > 0:
            if self.special_action == None:
                self.life_timer -= dt
                if self.life_timer <= 0:
                    self.special_action = 'activate'
                    self.special_action_timer = HP_PARADOX_DEFAULT_ACTIVATE_TIME
                    play_loop.knight.damage_ignore_iframe(self.paradox_dmg)
                    play_loop.knight.set_parapos(play_loop.knight.x, play_loop.knight.y, 0)
                else:
                    blink_speed = clamp(0.03, 0.02 + self.life_timer / 10, 0.5)
                    if self.blink_timer <= 0:
                        self.frame = 0
                        self.blink_timer = 1 + 0.1 / blink_speed
                    else:
                        self.blink_timer -= dt / blink_speed
                        if self.blink_timer > 1:
                            self.frame = 0
                        else:
                            self.frame = 1
            elif self.special_action == 'deactivate':
                self.special_action_timer -= dt
                self.frame = 4 + ((HP_PARADOX_DEFAULT_DEACTIVATE_TIME - self.special_action_timer) / HP_PARADOX_DEFAULT_DEACTIVATE_TIME * 4) % 4
                if self.special_action_timer <= 0:
                    self.delete = True
            else:
                self.special_action_timer -= dt
                self.frame = 8 + ((HP_PARADOX_DEFAULT_ACTIVATE_TIME - self.special_action_timer) / HP_PARADOX_DEFAULT_ACTIVATE_TIME * 8) % 8
                if self.special_action_timer <= 0:
                    self.delete = True

        if not self.delete:
            if self.special_action != 'despawn':
                world.collidecheck(self, "knight", "knightinarea")
                world.collidecheck(self, "monster", "monsterinarea")
        for case in self.collision:
            if case[0] in self.collisionchecked:
                pass
            else:
                if case[0].typename == "knight":
                    if self.hp_dmg == 0 and self.paradox_dmg>0 and self.life_timer > 0 and self.special_action!='deactivate':
                        if "knight" in self.damageto:
                            self.special_action = 'deactivate'
                            self.special_action_timer = HP_PARADOX_DEFAULT_DEACTIVATE_TIME
                            play_loop.knight.set_parapos(self.x, self.y, self.r)
                    elif self.hp_dmg>0 and self.life_timer <= 0:
                        if "knight" in self.damageto:
                            dirx, diry, _ = calculfuncs.facedircommon(self.x, self.y, case[0].x, case[0].y)
                            case[0].damageknockback(self.hp_dmg, self.paradox_dmg, self.knockback*dirx, self.knockback*diry)
                            self.collisionchecked.append(case[0])
            self.collision.remove(case)
        pass

    def draw(self):
        if self.hp_dmg!=0 and self.r<48:
            Area.damage_hp_area_image.clip_draw(int(self.frame) *32,0, 32, 32, int((self.x - play_loop.cam_x) / 2) * 2,int((self.y - play_loop.cam_y) / 2) * 2, 64, 64)
        elif self.hp_dmg==0 and self.paradox_dmg>0 and self.r>48:
            frame1=self.frame%8
            frame2=(self.frame-frame1)/8
            Area.damage_paradox_area_image.clip_draw(int(frame1) *80, int(1-frame2) *80, 80, 80, int((self.x - play_loop.cam_x) / 2) * 2,int((self.y - play_loop.cam_y) / 2) * 2, 160, 160)

    def sendfeedback(self,fdbk):
        self.feedback.append(fdbk)

    def deleteaction(self):
        pass