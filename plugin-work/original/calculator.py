""" A simple expression calculator.

See http://effbot.org/zone/simple-top-down-parsing.txt for detailed explanations
as to how it works.

This is the main file used to demonstrate plugin frameworks.  In this
example, we import known objects residing in separate python files explicitly
specified by name.
In a true plugin system, we would import arbitrary objects residing in
arbitrarily named files.
"""

import re

OPERATORS = {}

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
    return int(expression())

def init_operators():
    '''simulated plugin initializer'''
    import op_1, op_2
    OPERATORS['+'] = op_1.operator_add_token
    OPERATORS['-'] = op_1.operator_sub_token
    OPERATORS['*'] = op_1.operator_mul_token
    OPERATORS['/'] = op_1.operator_div_token
    OPERATORS['**'] = op_2.operator_pow_token

if __name__ == "__main__":
    init_operators()
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
