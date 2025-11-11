from pico2d import open_canvas, update_canvas,delay, close_canvas
import time

import play_loop as gameplaymode
import world

nextplaymode='gameplaymode'
reply='None'
canvas_width=1600
canvas_height=600

def getcanvasheight():
    return canvas_height

def changegamemode(next):
    global nextplaymode
    nextplaymode=next

open_canvas(canvas_width, canvas_height)
while True:
    if nextplaymode == 'quitgame': break
    elif nextplaymode == 'gameplaymode':
        gameplaymode.initscene()
        nextplaymode='None'
        while nextplaymode == 'None':
            world.deletemanage()
            world.collidemanage()
            gameplaymode.handle_events()
            reply=gameplaymode.update()
            if reply and reply!='None':
                nextplaymode=reply
            gameplaymode.draw()
close_canvas()