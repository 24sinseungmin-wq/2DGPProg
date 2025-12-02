from pico2d import *
import world,ui,interface,time
from knight import Knight
from slime import Slime
from area import Area
from shadow import Shadow

frame_time = 0.0
current_time = time.time()
knight=None
running=True
cam_x=0
cam_y=0

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
    global knight
    knight = Knight()
    knight.x=600
    knight.y=300
    monster = []
    world.add_object(knight,8)
    for i in range(5):
        monster.append(Slime(1200,300,'idle',0,True))
        world.add_object(monster[len(monster) - 1], 8)
    area=Area(1200,200,64,5.0,0,1,False,0)
    world.add_object(area,6)

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
    to_x=knight.x-400.0
    to_y=knight.y-400.0
    cam_x=to_x
    cam_y=to_y
    cam_x=to_x*(1-pow(0.01,frame_time))+cam_x*pow(0.01,frame_time)
    cam_y=to_y*(1-pow(0.01,frame_time))+cam_y*pow(0.01,frame_time)

def draw():
    clear_canvas()
    world.render()
    ui.render()
    update_canvas()

def finish():
    world.clear()

def pause():pass
def resume():pass