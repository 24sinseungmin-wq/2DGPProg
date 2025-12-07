from pico2d import *
import world,ui,interface,time
from knight import Knight
from slime import Slime
from shooter_slime import Shooter_Slime
from area import Area
from shadow import Shadow
from interactobj import Interactobj
from background import Background
frame_time = 0.0
current_time = time.time()
knight=None
running=True
cam_x=0
cam_y=0
background=None

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
    global background
    background=Background(4000,4000,False,0)
    world.add_object(background,0)
    global knight
    knight = Knight()
    knight.x=0
    knight.y=0
    monster = []
    world.add_object(knight,8)
    for i in range(5):
        monster.append(Shooter_Slime(1200,300,'idle',0,False))
        monster.append(Slime(1200,300,'idle',0,False))
    world.add_objects(monster, 8)
    area=Area(1200,200,64,5.0,0,1,False,0)
    world.add_object(area,6)
    shop=Interactobj(300,300,32,96,32,150,False,0,[["money",50]],[["max_hp",2]],["+1H","50G","1234567890"])
    world.add_object(shop,8)
    ui.uiinit(knight)

def update():
    global running
    if not running:
        finish()
        return 'quitgame'
    global frame_time,current_time
    frame_time = time.time() - current_time
    current_time += frame_time
    world.sortbypos(8)
    world.update()
    ui.update()
    camtoknight()

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

def setshop(x,y):
    text=[]
    if knight.level>3:

