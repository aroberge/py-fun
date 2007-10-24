'''util.py

utilies functions for froggie
'''
from pyglet.gl import *

def outside_world(obj, world):
    '''determine if an object has gone totally outside a world boundary.

       returns True if the object has left.
    This is useful for object that can be destroyed when they have
    left the world.
    '''
    if obj.x > world.x + world.width:
        return True
    elif obj.y > world.y + world.height:
        return True
    elif obj.x + obj.width < world.x:
        return True
    elif obj.y + obj.height < world.y:
        return True
    else:
        return False

def draw_rotated(obj, image):
    if obj.rotation == 0:
        image.blit(obj.x, obj.y)
    else:
        glLoadIdentity()
        # make the origin coincide with center of image, then rotate about
        # the z-axis
        glTranslatef(obj.x + obj.width/2, obj.y + obj.height/2, 0)
        glRotatef(obj.rotation, 0, 0, 1)
        # blit the rotated image so that the center of the image coincide
        # with the new origin
        image.blit(-obj.width/2, -obj.height/2)
        # restore previous coordinate system
        glRotatef(-obj.rotation, 0, 0, 1)
        glTranslatef(-obj.x - obj.width/2, -obj.y - obj.height/2, 0)


def detect_collision(obj, others, overlap):
    '''determines if a collision between a frog object "obj" and any given one
       in the list "others" has occurred.  All objects are expected
       to possess a height and a width attribute.

       Quits as soon as a collision is found,  returning True,
       or False if no collision is detected.

       Note that we make it so that it requires an overlap of a few pixels
       to declare a true collision.
    '''
    obj_x = obj.x
    obj_y = obj.y
    obj_max_x = obj_x + obj.width
    obj_max_y = obj_y + obj.height
    result = set()
    for other in others:
        if obj_x + overlap > other.x + other.width:
            continue
        elif obj_y > other.y + other.height:
            continue
        elif obj_max_x - overlap < other.x:
            continue
        elif obj_max_y < other.y:
            continue
        else:
            return other
    return False
