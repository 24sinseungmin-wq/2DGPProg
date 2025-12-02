import math
import random

def facedircommon(x, y, tx, ty):
    if x==tx and y==ty:
        tempdir=random.random()
    else:
        tempdir = math.atan2(x - tx, y - ty)
    dirx = -math.sin(tempdir)
    diry = -math.cos(tempdir)
    return dirx, diry, tempdir