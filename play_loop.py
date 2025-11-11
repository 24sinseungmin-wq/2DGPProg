from pico2d import *
import world,interface,time
from knight import Knight
from slime import Slime

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
    monster = []
    world.add_object(knight,8)
    monster.append(Slime())
    world.add_object(monster[len(monster)-1],8)

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
    #camtoknight()

def camtoknight():
    global cam_x
    global cam_y
    global knight
    to_x=knight.x-800.0
    to_y=knight.y-300.0
    cam_x=to_x
    cam_y=to_y
    #cam_x=to_x*(1-pow(0.01,frame_time))+cam_x*pow(0.01,frame_time)
    #cam_y=to_y*(1-pow(0.01,frame_time))+cam_y*pow(0.01,frame_time)

def draw():
    clear_canvas()
    world.render()
    update_canvas()

def finish():
    world.clear()

def pause():pass
def resume():pass