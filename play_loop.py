from pico2d import *
import world,interface,time
from knight import Knight

frame_time = 0.0
current_time = time.time()
knight=None
running=True

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
    world.add_object(knight,2)

def update():
    global running
    if not running:
        finish()
        return 'quitgame'
    global frame_time,current_time
    frame_time = time.time() - current_time
    current_time += frame_time
    world.update()

def draw():
    clear_canvas()
    world.render()
    update_canvas()

def finish():
    world.clear()

def pause():pass
def resume():pass