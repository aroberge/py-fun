""" A simple expression calculator.

See http://effbot.org/zone/simple-top-down-parsing.htm for detailed explanations
as to how it works.

This is the main file used to demonstrate plugin frameworks.
"""

import re

from plugins.base import OPERATORS, init_plugins

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
    assert calculate("2**3") == 8
    assert calculate("2*2**3") == 16
    print "Done!"
