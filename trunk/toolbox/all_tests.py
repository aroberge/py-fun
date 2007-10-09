'''
all_tests.py

Runs a series of tests contained in text files, using the doctest framework.
All the tests are asssumed to be located in the "toolbox/test" sub-directory.

A second series of tests used for comparing speed of various algorithms
is also available.
'''

import doctest
import os.path

doctest_files = [ "test_collisions.txt"]

import os
print os.getcwd()

for t in doctest_files:
   failure, nb_tests = doctest.testfile("test" + os.path.sep + t)
   print "%d failures in %d tests in file: %s"%(failure, nb_tests, t)


# Note that the number of tests, as identified by the doctest module
# is equal to the number of commands entered at the interpreter
# prompt; so this number is normally much higher than the number
# of test.


speedtests = {"collisions": True}

if speedtests["collisions"]:
    import test.speedtest_collisions
    test.speedtest_collisions.main()
