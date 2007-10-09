'''speedtest_collisions.py

Performs a series of speed test of various algorithms, using the timeit
module.
See main() to determine which tests should be run, and
do_test() to determine the test parameters.

A global test parameter, max_nb_objects, is defined at the
beginning of this file.

This module is meant to be run from a module (all_tests.py) located
it the parent directory of its own location.
'''
import math
import random
from timeit import Timer


max_nb_objects = 100000

class Mixed(object):
    '''a mixed test class that has the required attributes to
       be treated as a circle or as a rectangle'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.r = 16


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
        "setup": "from collisions import one_to_many_rectangle;"\
            "from test.speedtest_collisions import dense_primary, dense_target",
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
        "setup": "from collisions import one_to_many_rectangle;"\
            "from test.speedtest_collisions import sparse_primary, sparse_target",
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
        "setup": "from collisions import one_to_many_rectangle_detect;"\
            "from test.speedtest_collisions import dense_primary, dense_target",
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
        "setup": "from collisions import one_to_many_rectangle_detect;"\
            "from test.speedtest_collisions import sparse_primary, sparse_target",
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
        "setup": "from collisions import one_to_many_circle;"\
            "from test.speedtest_collisions import dense_primary, dense_target",
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
        "setup": "from collisions import one_to_many_circle;"\
            "from test.speedtest_collisions import sparse_primary, sparse_target",
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
        "setup": "from collisions import many_to_many_rectangle;"\
            "from test.speedtest_collisions import dense_primary, dense_target",
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
        "setup": "from collisions import many_to_many_rectangle;"\
            "from test.speedtest_collisions import sparse_primary, sparse_target",
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
        "setup": "from collisions import build_grid, collide_on_grid;"\
            "from test.speedtest_collisions import dense_primary, dense_target",
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
        "setup": "from collisions import build_grid, collide_on_grid;"\
            "from test.speedtest_collisions import sparse_primary, sparse_target",
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


def main():
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