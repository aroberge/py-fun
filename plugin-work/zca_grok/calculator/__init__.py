""" A simple expression calculator.

See  http://aroberge.blogspot.com/2008/12/plugins-part-3-simple-class-based.html
for an explanation.

This is the main file used to demonstrate plugin frameworks.
"""

import re

from zope import component

class literal_token(object):
    def __init__(self, value):
        self.value = value
    def nud(self):
        return self.value

class end_token(object):
    lbp = 0

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

from plugins.interfaces import IOperator
def tokenize(program):
    for number, operator in re.findall("\s*(?:(\d+)|(\*\*|.))", program):
        if number:
            yield literal_token(int(number))
        else:
            try:
                yield component.getUtility(IOperator, operator)
            except LookupError:
                raise SyntaxError("unknown operator: %r" % operator)
    yield end_token()

def calculate(program):
    global token, next
    next = tokenize(program).next
    token = next()
    return expression()
