import math

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
    elif requester.delete:
        return

    for layer in world:
        for o in layer:
            if o!=requester and o.typename==targettype and o.delete==False:
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
    global world,colide_checklist
    delete_list=[]
    for layer in world:
        for obj in layer:
            if hasattr(obj,'areas') and len(obj.areas)>0:
                for area in obj.areas:
                    if area.delete:
                        area.deleteaction()
                        obj.areas.remove(area)
    for layer in world:
        for o in layer:
            if o.delete:
                o.deleteaction()
                delete_list.append(o)
    for collide in collide_checklist:
        if collide[0] in delete_list or collide[1] in delete_list:
            collide_checklist.remove(collide)
    for layer in world:
        for o in layer:
            if not hasattr(o,'delete') or o.delete:
                remove_object(o)

def linedistcalcul(x1,y1,x2,y2,dotx,doty):
    vec_ab=(x2-x1,y2-y1)
    vec_ac=(dotx-x1,doty-y1)
    mul_ad=(vec_ab[0]*vec_ac[0]+vec_ab[1]*vec_ac[1])/(vec_ab[0]**2+vec_ab[1]**2)
    pos_d=(x1+mul_ad*(x2-x1),y1+mul_ad*(y2-y1))
    return pos_d

def damagecollide(damage, x1, y1, x2, y2, r, backmul, sidemul, targettype, attacker=None):
    global world
    for layer in world:
        for o in layer:
            if o.typename==targettype:
                dot_d=linedistcalcul(x1,y1,x2,y2,o.x,o.y)
                dist=0
                if (dot_d[0]-x1)*(dot_d[0]-x2)>0 or (dot_d[1]-y1)*(dot_d[1]-y2)>0:
                    #d1=math.sqrt((o.x - x1) ** 2 + (o.y - y1) ** 2)
                    d2=math.sqrt((o.x - x2) ** 2 + (o.y - y2) ** 2)
                    dist=d2#min(d1,d2)
                else:
                    dist=math.sqrt((dot_d[0]-o.x)**2+(dot_d[1]-o.y)**2)
                if dist<=r+o.r:
                    vec_knockback=[x2-x1,y2-y1] #크기를 1로 만들기
                    vec_knockside=[o.x-dot_d[0],o.y-dot_d[1]]  #크기를 1로 만들기
                    vec_knockback_mul=math.sqrt(vec_knockback[0]**2+vec_knockback[1]**2)*backmul
                    vec_knockside_mul=math.sqrt(vec_knockside[0]**2+vec_knockside[1]**2)*sidemul
                    vec_knockback[0]*=-vec_knockback_mul
                    vec_knockback[1]*=-vec_knockback_mul
                    vec_knockside[0]*=-vec_knockside_mul
                    vec_knockside[1]*=-vec_knockside_mul

                    vx=vec_knockback[0]*math.cos(((1/vec_knockback_mul)/(r+o.r))*(math.pi/2))+vec_knockside[0]*math.sin(((1/vec_knockside_mul)/(r+o.r))*0.75*(math.pi/2))
                    vy=vec_knockback[1]*math.cos(((1/vec_knockback_mul)/(r+o.r))*(math.pi/2))+vec_knockside[1]*math.sin(((1/vec_knockside_mul)/(r+o.r))*0.75*(math.pi/2))
                    if o.typename=="monster":
                        o.sendfeedback(("damage",attacker,damage))
                        o.sendfeedback(("knockback_hit",attacker,vx,vy))
                    #hit_knockback, 다중피격 안되게 hit/hit_knockback 상태에선 피해 안 주게 설정하기, 무적이나 에어본 상태에선 피해 안 주게 설정하기
                    #damage(),hit_knockback 설정하기
                    pass    #피격판정 추가
"""
damagecolide() 등을 모아두다 나중에 처리하는 기능 추가하기
"""

def sortbypos(layernum):
    global world
    world[layernum].sort(key=lambda object: object.y, reverse=True)