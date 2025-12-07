from pico2d import open_canvas, update_canvas,delay, close_canvas
import time

import play_loop as gameplaymode
import titlemode as titlemode
import world

import os
print(os.getenv('PYSDL2_DLL_PATH'))


nextplaymode='titlemode_reset'
reply='None'
canvas_width=800
canvas_height=800

def getcanvaswidth():
    return canvas_width
def getcanvasheight():
    return canvas_height

def changegamemode(next):
    global nextplaymode
    nextplaymode=next

open_canvas(canvas_width, canvas_height)
while True:
    if nextplaymode == 'quitgame': break
    elif nextplaymode == 'titlemode_reset':
        titlemode.initscene()
        nextplaymode='None'
        while nextplaymode == 'None':
            titlemode.handle_events()
            reply=titlemode.update()
            if reply and reply!='None':
                nextplaymode=reply
            titlemode.draw()
    elif nextplaymode == 'gameplaymode_reset':
        gameplaymode.initscene()
        nextplaymode='None'
        while nextplaymode == 'None':
            world.collidemanage()
            world.deletemanage()
            gameplaymode.handle_events()
            reply=gameplaymode.update()
            if reply and reply!='None':
                nextplaymode=reply
            gameplaymode.draw()
    elif nextplaymode == 'gameplaymode':
        nextplaymode='None'
        while nextplaymode == 'None':
            world.collidemanage()
            world.deletemanage()
            gameplaymode.handle_events()
            reply=gameplaymode.update()
            if reply and reply!='None':
                nextplaymode=reply
            gameplaymode.draw()
close_canvas()