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
start=False
cam_x=0
cam_y=0
background=None

def handle_events():
    global running
    global start
    global x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            start = True

def initscene():
    pass

def update():
    global running
    if not running:
        finish()
        return 'quitgame'
    elif start:
        finish()
        return 'gameplaymode_reset'
    global frame_time,current_time
    frame_time = time.time() - current_time
    current_time += frame_time
    ui.update()

def draw():
    clear_canvas()
    update_canvas()

def finish():
    world.clear()

def pause():pass
def resume():pass