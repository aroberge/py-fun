""" A simple expression calculator entirely contained in a single file.

See http://aroberge.blogspot.com/2008/12/plugins-part-1-application.html
for an explanation.

This is the basic application used to demonstrate various plugin frameworks.
"""

import re

class literal_token(object):
    def __init__(self, value):
        self.value = value
    def nud(self):
        return self.value

class operator_add_token(object):
    lbp = 10
    def nud(self):
        return expression(100)
    def led(self, left):
        return left + expression(10)

class operator_sub_token(object):
    lbp = 10
    def nud(self):
        return -expression(100)
    def led(self, left):
        return left - expression(10)

class operator_mul_token(object):
    lbp = 20
    def led(self, left):
        return left * expression(20)

class operator_div_token(object):
    lbp = 20
    def led(self, left):
        return left / expression(20)

class operator_pow_token(object):
    lbp = 30
    def led(self, left):
        return left ** expression(30-1)

class end_token(object):
    lbp = 0

def tokenize(program):
    for number, operator in re.findall("\s*(?:(\d+)|(\*\*|.))", program):
        if number:
            yield literal_token(int(number))
        elif operator == "+":
            yield operator_add_token()
        elif operator == "-":
            yield operator_sub_token()
        elif operator == "*":
            yield operator_mul_token()
        elif operator == "/":
            yield operator_div_token()
        elif operator == "**":
            yield operator_pow_token()
        else:
            raise SyntaxError("unknown operator: %r" % operator)
    yield end_token()

def expression(rbp=0):  # note that expression is a global object in this module
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
    assert calculate("5-1-2") == 2
    print "Done!"
