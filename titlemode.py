from pico2d import *
import time
frame_time = 0.0
current_time = time.time()
knight=None
running=True
start=False
cam_x=0
cam_y=0
image=None

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
    global image,running,start
    running=True
    start=False
    if image is None:
        image = load_image('temptitle.png')
    pass

def update():
    global running,start
    if not running:
        finish()
        return 'quitgame'
    elif start:
        start=False
        finish()
        return 'gameplaymode_reset'
    global frame_time,current_time
    frame_time = time.time() - current_time
    current_time += frame_time

def draw():
    global image
    clear_canvas()
    image.draw_to_origin(0,0,800,800)
    update_canvas()

def finish():
    pass

def pause():pass
def resume():pass