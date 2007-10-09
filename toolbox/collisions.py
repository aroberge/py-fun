'''collisions.py

module containing a number of functions to determine if a collision
(with various possible cases) has occurred.  Most of these functions
currently rely on objects being represented (or bounded) by rectangles
except for two which assumes objects bounded by circles.

One advantage of using these utility functions is that they are tested,
and do not need to be re-implemented every time a new class of objects
is created.  An other potential advantage is that they can be replaced
easily by other functions (e.g. if a pixel-perfect detection is needed),
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
    (True, set(objects_with_which_collision_occurred))'''
    # define some local variables for optimal speed
    obj_x = obj.x
    obj_y = obj.y
    obj_max_x = obj_x + obj.width
    obj_max_y = obj_y + obj.height
    result = set()
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
            result.add(other)
    if result:
        return True, result
    else:
        return False

def one_to_many_rectangle_detect(obj, others):
    '''determines if a collision between a object "obj" and any given one
       in the list "others" has occurred.  All objects are expected
       to possess a height and a width attribute.

       Quits as soon as a collision is found,  returning True,
       or False if no collision is detected'''
    # define some local variables for optimal speed
    obj_x = obj.x
    obj_y = obj.y
    obj_max_x = obj_x + obj.width
    obj_max_y = obj_y + obj.height
    result = set()
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
            return True
    return False

def many_to_many_rectangle(objs, others):
    '''determines if collisions have occurred between a list of objects
       and a second list of "others".  All objects are expected to possess
       a height and a width attribute.

       Returns either an empty list or a list containing elements
          (object, (objects_with_which_collision_occurred))

       This simple implementation calls another function.
    '''
    result = []
    for obj in objs:
        res = one_to_many_rectangle(obj, others)
        if res is not False:
            for r in res[1]:
                result.append((obj, r))
    return result

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

def one_to_many_circle(obj, others):
    '''determines if a collision between a object "obj" and any given one
       in the list "others" has occurred.  All objects are expected
       to possess a radius attribute.

    Returns either False, or
    (True, set(objects_with_which_collision_occurred))'''
    # define some local variables for optimal speed
    obj_min_x = obj.x - obj.r
    obj_min_y = obj.y - obj.r
    obj_max_x = obj.x + obj.r
    obj_max_y = obj.y + obj.r
    result = set()
    for other in others:
        if obj_min_x > other.x + other.r:
            continue
        elif obj_min_y > other.y + other.r:
            continue
        elif obj_max_x < other.x - other.r:
            continue
        elif obj_max_y < other.y - other.r:
            continue
        elif (obj.x - other.x)**2 + (obj.y - other.y)**2 > (obj.r + other.r)**2 :
            continue
        else:
            result.add(other)
    if result:
        return True, result
    else:
        return False

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

def build_grid(objs, resolution):
    '''creates a dict containing a grid cell in which an object is located.
       The grid cells have size "resolution", and the dict item is a list
       of objects'''
    grid = {}
    for obj in objs:
        for i in range(obj.x//resolution, (obj.x + obj.width)//resolution + 1):
            for j in range(obj.y//resolution, (obj.y + obj.height)//resolution + 1):
                key = (i, j)
                if key in grid:
                    grid[key].append(obj)
                else:
                    grid[key] = [obj]
    return grid

def collide_on_grid(grid_obj, grid_other):
    result = set()
    for key in grid_obj:
        if key in grid_other:
            for obj in grid_obj[key]:
                res = one_to_many_rectangle(obj, grid_other[key])
                if res is not False:
                    for r in res[1]:
                        result.add((obj, r))
    return result


def estimate_speed(statement, setup, target_time, max_nb_objects, nb_times,
                   nb_variables):
    repeat1, repeat2, repeat3 = (20, 20, 40)
    nb_repeats = repeat1 + repeat2 + repeat3*nb_times
    print "Estimated time for this test = %0.2f sec"%(nb_repeats*target_time)
    # crude test
    nb_objects = min(20, max_nb_objects)
    time1 = speed_test(statement%(0), setup, target_time, nb_objects, nb_variables, repeat1)
    # estimate the right number of object based on crude test result
    if nb_variables:
        factor = target_time/time1
    else:
        factor = (target_time/time1)**0.5
    nb_objects *= factor
    #print "factor = ", factor,
    nb_objects = int(min(nb_objects, max_nb_objects))
    # repeat the test using the estimate
    time2 = speed_test(statement%(0), setup, target_time, nb_objects, nb_variables, repeat2)
    #repeat the whole process once more to refine the estimate
    if nb_variables:
        factor = target_time/time2
    else:
        factor = (target_time/time2)**0.5
    nb_objects *= factor
    #print  "%.2f"%factor,
    nb_objects = int(min(nb_objects, max_nb_objects))
    n = []
    t = []
    for i in range(nb_times):
        t1 = speed_test(statement%i, setup,target_time, nb_objects, nb_variables, repeat3)
        n.append(nb_objects)
        t.append(t1)
        if nb_variables:
            factor = target_time/t1
        else:
            factor = 0.5 + 0.5*(target_time/t1)**0.5
            factor
        factor = min(1.25, factor)
        factor = max(factor, 0.8)
        #print  "%.2f"%factor,
        nb_objects *= factor
        nb_objects = int(nb_objects)
    nb_objects = int(min(nb_objects, max_nb_objects))
    ave_nb_objects, std = do_stats(n, t, target_time)
    return int(ave_nb_objects), int(std)

def speed_test(statement, setup, target_time, nb_objects, nb_variables, repeat):
    if nb_variables == 1:
        full_statement = statement%nb_objects
    elif nb_variables == 2:
        full_statement = statement%(nb_objects, nb_objects)
    t = Timer(full_statement, setup)
    time1 = t.timeit(number=repeat)/repeat
    return time1

def do_stats(n, t, target_framerate):
    '''computes the average and standard deviation'''
    #print "\n", n
    # compute average
    ave = 0
    for n1 in n:
        ave += n1
    ave /= nb_times
    # compute standard deviation
    std = 0
    for n1 in n:
        std += (n1 - ave)**2
    std /= nb_times
    std = std**0.5
    return int(ave), int(std)

def do_test(name, max_nb_objects):
    global nb_times
    test_parameters = {
    "one_to_many_rectangle (dense)":
        {"nb_times": 30,
         "fps":300,
        "statement": "one_to_many_rectangle(dense_primary[%d], dense_target[:%%d])",
        "setup": "from __main__ import one_to_many_rectangle, dense_primary, dense_target",
        "nb_variables": 1,
        "result": "nb of objects = %d (standard deviation = %d)",
        "comment": """\
Note: this test is highly dependent on the specific configuration.
This is the cause of the relatively large standard deviation."""
        },
    "one_to_many_rectangle (sparse)":
        {"nb_times": 30,
         "fps":300,
        "statement": "one_to_many_rectangle(sparse_primary[%d], sparse_target[:%%d])",
        "setup": "from __main__ import one_to_many_rectangle, sparse_primary, sparse_target",
        "nb_variables": 1,
        "result": "nb of objects = %d (standard deviation = %d)",
        "comment": """\
Note: this test is highly dependent on the specific configuration.
This is the cause of the relatively large standard deviation."""
        },
    "one_to_many_rectangle_detect (dense)":
        {"nb_times": 30,
         "fps":1000,
        "statement": "one_to_many_rectangle_detect(dense_primary[%d], dense_target[:%%d])",
        "setup": "from __main__ import one_to_many_rectangle_detect, dense_primary, dense_target",
        "nb_variables": 1,
        "result": "nb of objects = %d (standard deviation = %d)",
        "comment": """\
Note: Collisions are found so quickly on dense system that the number of
target objects that can be apparently handle is huge! You should use very high
fps value for the test so that the target frame_rate is small.
The standard deviation value is also normally huge, pointing out the
extremely high dependency on initial values."""
        },
    "one_to_many_rectangle_detect (sparse)":
        {"nb_times": 30,
         "fps":300,
        "statement": "one_to_many_rectangle_detect(sparse_primary[%d], sparse_target[:%%d])",
        "setup": "from __main__ import one_to_many_rectangle_detect, sparse_primary, sparse_target",
        "nb_variables": 1,
        "result": "nb of objects = %d (standard deviation = %d)",
        "comment": """\
Note: this test is highly dependent on the specific configuration.
This is the cause of the relatively large standard deviation."""
        },
    "one_to_many_circle (dense)":
        {"nb_times": 30,
         "fps":300,
        "statement": "one_to_many_circle(dense_primary[%d], dense_target[:%%d])",
        "setup": "from __main__ import one_to_many_circle, dense_primary, dense_target",
        "nb_variables": 1,
        "result": "nb of objects = %d (standard deviation = %d)",
        "comment": """\
Note: this test is highly dependent on the specific configuration.
This is the cause of the relatively large standard deviation."""
        },
    "one_to_many_circle (sparse)":
        {"nb_times": 30,
         "fps":300,
        "statement": "one_to_many_circle(sparse_primary[%d], sparse_target[:%%d])",
        "setup": "from __main__ import one_to_many_circle, sparse_primary, sparse_target",
        "nb_variables": 1,
        "result": "nb of objects = %d (standard deviation = %d)",
        "comment": """\
Note: this test is highly dependent on the specific configuration.
This is the cause of the relatively large standard deviation."""
        },
    "many_to_many_rectangle (dense)":
        {"nb_times": 20,
         "fps":30,
        "statement": "many_to_many_rectangle(dense_primary[%d:%%d], dense_target[:%%d])",
        "setup": "from __main__ import many_to_many_rectangle, dense_primary, dense_target",
        "nb_variables": 2,
        "result": "nb of objects = %d x %d (standard deviation = %d)",
        "comment": """\
Note: The calculation is done for the speed test assuming the same number of
'object' and 'targets'.  This method is quadratic in the number of
objects/target and is not as efficient as the collide_on_grid function."""
        },
    "many_to_many_rectangle (sparse)":
        {"nb_times": 20,
         "fps":30,
        "statement": "many_to_many_rectangle(sparse_primary[%d:%%d], sparse_target[:%%d])",
        "setup": "from __main__ import many_to_many_rectangle, sparse_primary, sparse_target",
        "nb_variables": 2,
        "result": "nb of objects = %d x %d (standard deviation = %d)",
        "comment": """\
Note: The calculation is done for the speed test assuming the same number of
'object' and 'targets'.  This method is quadratic in the number of
objects/target and is not as efficient as the collide_on_grid function.
This can especially be seen on sparse systems."""
        },
    "collide_on_grid (dense)":
        {"nb_times": 20,
         "fps":30,
        "statement": """\
grid_primary = build_grid(dense_primary[%d:%%d], resolution=30)
grid_target = build_grid(dense_target[:%%d], resolution=30)
collide_on_grid(grid_primary, grid_target)""",
        "setup": "from __main__ import collide_on_grid, build_grid, dense_primary, dense_target",
        "nb_variables": 2,
        "result": "nb of objects = %d x %d (standard deviation = %d)",
        "comment": """\
Note: The calculation is done for the speed test assuming the same number of
'object' and 'targets'.  This method is linear in the number of
objects/target and is thus more efficient than many_to_many_rectangle().
This can especially be seen on sparse systems."""
        },
    "collide_on_grid (sparse)":
        {"nb_times": 20,
         "fps":30,
        "statement": """\
grid_primary = build_grid(sparse_primary[%d:%%d], resolution=30)
grid_target = build_grid(sparse_target[:%%d], resolution=30)
collide_on_grid(grid_primary, grid_target)""",
        "setup": "from __main__ import collide_on_grid, build_grid, sparse_primary, sparse_target",
        "nb_variables": 2,
        "result": "nb of objects = %d x %d (standard deviation = %d)",
        "comment": """\
Note: The calculation is done for the speed test assuming the same number of
'object' and 'targets'.  This method is linear in the number of
objects/target and is thus more efficient than many_to_many_rectangle().
This can especially be seen on sparse systems."""
        }
    }

    print "doing test: ", name
    print test_parameters[name]["comment"]
    print "- " * 30
    nb_times = test_parameters[name]["nb_times"]
    fps = test_parameters[name]["fps"]
    target_framerate = 1./fps
    statement = test_parameters[name]["statement"]
    setup = test_parameters[name]["setup"]
    nb_variables = test_parameters[name]["nb_variables"]
    result = test_parameters[name]["result"]
    print "target time per frame is:%0.2e"%target_framerate
    print "This corresponds to %0.1f frames per second"%fps
    ave_nb_objects, std = estimate_speed(statement, setup,
                    target_framerate, max_nb_objects, nb_times, nb_variables)
    print "-"*50
    if nb_variables == 1:
        print result%(ave_nb_objects, std)
    elif nb_variables == 2:
        print result%(ave_nb_objects, ave_nb_objects, std)
    else:
        print "Fatal error; wrong value for nb_variables: ", nb_variables
        import sys
        sys.exit()
    print "=" * 60, "\n"


if __name__ == "__main__":
    # first, testing code validity
    import doctest
    failures, nb_tests = doctest.testfile("test_collisions.txt")
    print "%d failures in %d tests in test_collisions.txt"%(failures, nb_tests)
    global dense_primary, dense_target, sparse_primary, sparse_target

    if failures == 0:
        # next, testing code speed
        import math
        import random
        from timeit import Timer

        class Mixed(object):
            '''a mixed test class that has the required attributes to
               be treated as a circle or as a rectangle'''
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.width = 32
                self.height = 32
                self.r = 16

        max_nb_objects = 100000
        print "generating lists of %d objects"%max_nb_objects
        print "this could take some time"
        # dense primary objects i.e. many objects in small "world"
        dense_primary = [Mixed(random.randint(0, 1000), random.randint(0, 1000))
                      for i in range(max_nb_objects)]
        print "25%% done; if this is too long, quit by pressing ctrl-c"\
              " and change the value of max_nb_objects"
        # dense target objects i.e. many objects in small "world"
        dense_target = [Mixed(random.randint(0, 1000), random.randint(0, 1000))
                      for i in range(max_nb_objects)]
        # sparse primary objects i.e. many objects in large "world"
        sparse_primary = [Mixed(random.randint(0, 1000000), random.randint(0, 1000000))
                      for i in range(max_nb_objects)]
        # sparse target objects i.e. many objects in large "world"
        sparse_target = [Mixed(random.randint(0, 1000000), random.randint(0, 1000000))
                      for i in range(max_nb_objects)]

        tests_to_do = [
        ("one_to_many_rectangle (dense)", True),
        ("one_to_many_rectangle (sparse)", True),
        ("one_to_many_rectangle_detect (dense)", True),
        ("one_to_many_rectangle_detect (sparse)", True),
        ("one_to_many_circle (dense)", True),
        ("one_to_many_circle (sparse)", True),
        ("many_to_many_rectangle (dense)", True),
        ("many_to_many_rectangle (sparse)", True),
        ("collide_on_grid (dense)", True),
        ("collide_on_grid (sparse)", True)
        ]

        print "\n", "+"*60, "\n"
        for test in tests_to_do:
            if test[1]:
                do_test(test[0], max_nb_objects)
        print "\nRemember: speed tests can be run on selected functions."
        print "Look at the end of the source file for details.\n"