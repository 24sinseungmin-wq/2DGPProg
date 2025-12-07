from pico2d import *
import world,ui,interface,time
from knight import Knight
from slime import Slime
from shooter_slime import Shooter_Slime
from area import Area
from shadow import Shadow
from interactobj import Interactobj, setshop_armor,setshop_potions,setshop_sword
from background import Background
from random import randint

from ui import paradoxeffecttimer

frame_time = 0.0
current_time = time.time()
knight=None
running=True
to_title=False
cam_x=0
cam_y=0
background=None
while_wave=False
wavenum=0
paradoxeffecttimer=0.0

def handle_events():
    global running
    global x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            interface.process_mouse(type=event.type,x=event.x,y=event.y)
        elif event.type == SDL_MOUSEBUTTONUP or event.type == SDL_MOUSEBUTTONDOWN:
            interface.process_mouse(type=event.type,button=event.button,x=event.x,y=event.y)
        elif event.type == SDL_MOUSEWHEEL:
            interface.process_mouse(type=event.type,x=event.x,y=event.y)

def initscene():
    world.clear()
    ui.clear()
    global background
    global wavenum
    global to_title
    to_title = False
    wavenum=1
    background=Background(4000,4000,False,0)
    world.add_object(background,0)
    global knight
    knight = Knight()
    knight.x=0
    knight.y=0
    monster = []
    world.add_object(knight,8)
    start_wave(0,0,32)
    ui.uiinit(knight)

def update():
    global running
    if not running:
        finish()
        return 'quitgame'
    global to_title
    if to_title:
        finish()
        return 'titlemode_reset'
    global frame_time,current_time
    frame_time = time.time() - current_time
    current_time += frame_time
    world.sortbypos(8)
    world.update()
    ui.update()
    camtoknight()
    if while_wave:
        while_wave_func(0,0)

def camtoknight():
    global cam_x
    global cam_y
    global knight
    to_x=clamp((-background.w/4),knight.x-400.0,(background.w/4-800))
    to_y=clamp((-background.h/4),knight.y-400.0,(background.h/4-800))
    cam_x=to_x
    cam_y=to_y

def draw():
    clear_canvas()
    world.render()
    ui.render()
    update_canvas()

def finish():
    world.clear()

def pause():pass
def resume():pass

def start_wave(x,y,r):#if not while_wave and...
    global wavenum,while_wave
    print(wavenum)
    world.clearshopobj()
    moblist=[]
    ticket = randint(3+3*int(wavenum),9 + 6*int(wavenum))
    ticket+= (randint(int(wavenum/4),int(wavenum))**2)
    while ticket>0:
        if randint(1,5)<=2 and ticket>=10 and wavenum>=4:
            ticket-=12
            moblist.append("Slime_rev")
        elif randint(1,5)<=2 and ticket>=7 and wavenum>=4:
            ticket-=9
            moblist.append("Proj_Slime_rev")
        elif randint(1,5)<=3 and ticket>=3 and wavenum>=2:
            ticket-=5
            moblist.append("Proj_Slime")
        elif randint(1,5)<=4:
            ticket-=3
            moblist.append("Slime")
    for mob in moblist:
        newmob=None
        tx=x+(randint(0,1)*2-1)*randint(150,500)
        ty=y+(randint(0,1)*2-1)*randint(150,500)
        if mob=="Slime":
            newmob=Slime(tx,ty,"stagger",20,False)
        elif mob=="Proj_Slime":
            newmob=Shooter_Slime(tx,ty,"stagger",20,False)
        elif mob=="Slime_rev":
            newmob=Slime(tx,ty,"stagger",0,True)
        elif mob=="Proj_Slime_rev":
            newmob=Shooter_Slime(tx,ty,"stagger",0,True)
        world.add_object(newmob,8)
    wavenum+=1
    while_wave=True
    return

def while_wave_func(x=0,y=0):#if while_wave
    global while_wave
    if not world.mobcheck():
        while_wave=False
        print(knight.money)
        knight.x,knight.y=x,y
        knight.vx,knight.vy=0,0
        knight.state="stagger"
        setshop_armor(x+100,y-100)
        setshop_sword(x,y-75)
        setshop_potions(x-100,y-100)
        warp=Interactobj(x,y+150,16,pw=0,ph=0,pr=0,reverse=False,imagetype=3,price=[],give=[["trigger_wave"]],text=[])
        world.add_object(warp,8)

