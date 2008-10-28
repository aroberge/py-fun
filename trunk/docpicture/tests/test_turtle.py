import unittest
# Ensuring that the proper path is found; there must be a better way
import os
import sys
sys.path.insert(0, os.path.normpath(os.path.join(os.getcwd(), "..", "..")))
# other imports proceed

from parsers import turtle

class TestTurtle(unittest.TestCase):
    ''' description '''
    def setUp(self):
        self.t = turtle.Turtle()

    def testFunctionName(self):
        pass


if __name__ == '__main__':
    unittest.main()