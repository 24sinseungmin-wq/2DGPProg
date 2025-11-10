
from knight import Knight
from pico2d import *
import play_loop

toggleL=False
toggleR=False

def getcanvasheight():
    return 600

def process_mouse(type='No input',button='No input',x='No input',y='No input'):
    global toggleL,toggleR
    print(f'Type={type},Button={button},x={x},y={y}')
    pass
    if type==1024:
        if toggleL == True:
            play_loop.knight.control('faceto', x, getcanvasheight() - y)
        elif toggleR == True:
            play_loop.knight.control('startstepto', x, getcanvasheight() - y)
    elif type==1025:
        if button == 1:
            toggleL=True
            play_loop.knight.control('attackcharge',x,getcanvasheight()-y)
        elif button==3:
            toggleR=True
            if toggleL==False:
                play_loop.knight.control('startstepto',x,getcanvasheight()-y)
    elif type==1026:
        if button==1:
            toggleL=False
            play_loop.knight.control('attackrelease',x,getcanvasheight()-y)
        elif button==3:
            toggleR=False
            if toggleL==False:
                play_loop.knight.control('idle',x,getcanvasheight()-y)
    #휠스크롤로 'potion'?
