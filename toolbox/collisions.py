'''collisions.py

module containing a number of functions to determine if a collision
(with various possible cases) has occurred.  Most of these functions
currently rely on objects being represented (or bounded) by rectangles
except for one which assumes objects bounded by circles.

One advantage of using these utility functions is that they are tested,
and do not need to be re-implemented every time a new class of objects
is created.  An other potential advantage is that they can be replaced
by other functions (e.g. if a pixel-perfect detection is needed),
with all of the code residing in a single module.
'''

def one_to_one_rectangle(obj, other):
    '''determines if a collision between a object "obj" and
       a single other "other" has occurred.  Both objects are expected to
       be rectangle-like, i.e. to possess a height and a width attribute.
    '''
    if obj.x > other.x + other.width:
        return False
    elif obj.y > other.y + other.height:
        return False
    elif obj.x + obj.width < other.x:
        return False
    elif obj.y + obj.height < other.y:
        return False
    else:
        return True

def one_to_many_rectangle(obj, others):
    '''determines if a collision between a object "obj" and any given one
       in the list "others" has occurred.  All objects are expected
       to possess a height and a width attribute.

    Returns either False, or
    (True, first_object_with_which_collision_occurred)'''
    # define some local variables for optimal speed
    obj_x = obj.x
    obj_y = obj.y
    obj_max_x = obj_x + obj.width
    obj_max_y = obj_y + obj.height
    for other in others:
        if obj_x > other.x + other.width:
            continue
        elif obj_y > other.y + other.height:
            continue
        elif obj_max_x < other.x:
            continue
        elif obj_max_y < other.y:
            continue
        else:
            return True, other
    return False


def one_to_one_circle(obj, other):
    '''determines if a collision between two objects ("obj" and "other")
       bounded by a circle has occurred.
       The location of both objects is expected to be that of the
       center of the circle, and both objects are expected to have a
       radius (r) attribute.'''
    # First, a simple check based on bounding rect to exclude most commonly
    # expected case
    if obj.x - obj.r > other.x + other.r:
        return False
    elif obj.y - obj.r > other.y + other.r:
        return False
    elif obj.x + obj.r < other.r - other.r:
        return False
    elif obj.y + obj.r < other.y - other.r:
        return False
    # next, the more precise and mathematically correct test
    elif (obj.x - other.x)**2 + (obj.y - other.y)**2 > (obj.r + other.r)**2 :
        return False
    else:
        return True

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

def leaving_world(obj, world):
    '''determine if an object is going through a world boundary.

       returns flag, (flag_x, Dx), (flag_y, Dy)

       flag: False if obj is totally inside world; True otherwise
       flag_x: True if going over X boundary
       Dx: non-zero if outside the world
              == obj.max_x - world.max_x (positive) if obj.max_x > world.max_x
              == obj.min_x - world.min_x (negative) if obj.min_x < world.min_x
       flag_y: True if going over Y boundary
       Dy: non-zero if outside the world
              == obj.max_y - world.max_y (positive) if obj.max_y > world.max_y
              == obj.min_y - world.min_y (negative) if obj.min_y < world.min_y

    This could be useful for objects that bounce off the world boundary,
    for example; however, a direct implementation would probably be more
    efficient.
    '''
    if obj.x + obj.width > world.x + world.width:
        flag_x = True
        Dx = (obj.x + obj.width) - (world.x + world.width)
    elif obj.x  < world.x:
        flag_x = True
        Dx = obj.x - world.x
    else:
        flag_x = False
        Dx = 0

    if obj.y + obj.height > world.y + world.height:
        flag_y = True
        Dy = (obj.y + obj.height) - (world.y + world.height)
    elif obj.y  < world.y:
        flag_y = True
        Dy = obj.y - world.y
    else:
        flag_y = False
        Dy = 0

    if flag_x or flag_y:
        return True, (flag_x, Dx), (flag_y, Dy)
    else:
        return False, (False, 0), (False, 0)

if __name__ == "__main__":
    # first, testing code validity
    import doctest
    failures, nb_tests = doctest.testfile("test_collisions.txt")
    print "%d failures in %d tests in test_collisions.txt"%(failures, nb_tests)
    global obj_test, others_test

    if failures == 0:
        # next, testing code speed
        import random
        from timeit import Timer
        target_framerate = 1./20

        class Rect(object):
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.width = 16
                self.height = 16

        class Circ(object):
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.radius = 16

        print "Testing one_to_many_rectangle()\n======================"
        nb_objects = 100
        max_time = 0.
        while max_time < target_framerate and nb_objects < 100000:
            nb_objects *= 2
            obj_test = Rect(500, 500)
            #Note: most of the time appears to be taken by this list creation
            others_test = [Rect(random.randint(0, 1000), random.randint(0, 1000))
                      for i in range(nb_objects)]
            t = Timer("one_to_many_rectangle(obj_test, others_test)",
                "from __main__ import one_to_many_rectangle, obj_test, others_test")
            max_time = t.timeit(number=1)
            print "time taken by many() for %d objects is %0.2e seconds"%(
                                                            nb_objects, max_time)
