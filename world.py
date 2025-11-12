world = [[] for _ in range(12)]
collide_checklist = []

def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

    raise ValueError('Cannot delete non existing object')

def clear():
    global world

    for layer in world:
        layer.clear()

def collidecheck(requester,targettype,reason="undefined"):
    global world, collide_checklist

    findreq=False
    for layer in world:
        if requester in layer:
            findreq=True
    if findreq==False:
        raise ValueError('Cannot check collision with non existing object')

    for layer in world:
        for o in layer:
            if o!=requester and o.typename==targettype:
                if (requester.x-o.x)**2+(requester.y-o.y)**2<(requester.r+o.r)**2:
                    collide_checklist.append([requester,o,reason])

def collidemanage():
    global world, collide_checklist
    for collide in collide_checklist:
        findreq=False
        findo=False
        for layer in world:
            if collide[0] in layer:
                findreq=True
            if collide[1] in layer:
                findo=True
            if findreq and findo:
                break
        if findreq==False or findo==False:
            raise ValueError('Cannot manage collision with non existing object(s)')
        collide[0].collision.append([collide[1],collide[2]])
        collide[1].collision.append([collide[0],collide[2]])
    collide_checklist = []

def deletemanage():
    global world
    for layer in world:
        for o in layer:
            if o.delete:
                remove_object(o)

def sortbypos(layernum):
    global world
    world[layernum].sort(key=lambda object: object.y, reverse=True)