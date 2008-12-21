""" A simple expression calculator.

See http://aroberge.blogspot.com/2008/12/plugins-part-5-activation-and.html
for details.

This is the main file used to demonstrate plugin frameworks.
"""

import os
import sys
import re

from plugins.base import OPERATORS, init_plugins, activate, deactivate,\
                         register_plugins

class literal_token(object):
    def __init__(self, value):
        self.value = value
    def nud(self):
        return self.value

class end_token(object):
    lbp = 0

def tokenize(program):
    for number, operator in re.findall("\s*(?:(\d+)|(\*\*|.))", program):
        if number:
            yield literal_token(int(number))
        elif operator in OPERATORS:
            yield OPERATORS[operator]()
        else:
            raise SyntaxError("unknown operator: %r" % operator)
    yield end_token()

def expression(rbp=0):
    global token
    t = token
    token = next()
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next()
        left = t.led(left)
    return left

def calculate(program):
    global token, next
    next = tokenize(program).next
    token = next()
    return expression()

if __name__ == "__main__":
    init_plugins(expression)
    assert calculate("+1") == 1
    assert calculate("-1") == -1
    assert calculate("10") == 10
    assert calculate("1+2") == 3
    assert calculate("1+2+3") == 6
    assert calculate("1+2-3") == 0
    assert calculate("1+2*3") == 7
    assert calculate("1*2+3") == 5
    assert calculate("6*2/3") == 4

    # "**" has not been activated at the start in base.py
    try:
        assert calculate("2**3") == 8
    except SyntaxError:
        print "Correcting error..."
        activate("**")
    assert calculate("2*2**3") == 16

    deactivate('+')
    try:
        assert calculate("1+2") == 3
    except SyntaxError:
        activate('+')
    assert calculate("1+2") == 3

    # Simulating dynamic external plugin initialization
    external_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              'external')
    sys.path.insert(0, external_dir)
    mod = __import__('op_3')
    mod.expression = expression
    # register this plugin using our default method
    register_plugins()
    # Since it is not activated by default, we need to do it explictly
    activate('%')
    assert calculate("7%2") == 1

    print "Done!"
