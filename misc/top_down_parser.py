''' Implementing parser from

from http://effbot.org/zone/simple-top-down-parsing.htm

'''

import re

token_pat = re.compile("\s*(?:(\d+)|(.))")
# nud = null denotation; when a token appears at the beginning of a construct
# led = left denotation) when it appears inside the construct
#       (to the left of the rest of the construct, that is)
# lbp = binding power; controls operator precedence

def expression(rbp=0):
    global token, next
    t = token
    token = next()
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next()
        left = t.led(left)
    return left

def tokenize(program):
    for number, operator in token_pat.findall(program):
        if number:
            yield literal_token(number)
        elif operator == "+":
            yield operator_add_token()
        elif operator == "-":
            yield operator_sub_token()
        elif operator == "*":
            yield operator_mul_token()
        elif operator == "/":
            yield operator_div_token()
        else:
            raise SyntaxError("unknown operator: %s" % operator)
    yield end_token()

def parse(program):
    global token, next
    next = tokenize(program).next
    token = next()
    return expression()


class literal_token(object):
    ''' and integer'''
    def __init__(self, value):
        self.value = int(value)
    def nud(self):
        return self.value

class operator_add_token(object):
    '''addition operator token'''
    lbp = 10
    def led(self, left):
        right = expression(10)
        return left + right

class operator_sub_token:
    lbp = 10
    def led(self, left):
        return left - expression(10)

class operator_mul_token:
    lbp = 20
    def led(self, left):
        return left * expression(20)

class operator_div_token:
    lbp = 20
    def led(self, left):
        return left / expression(20)

class end_token(object):
    '''denotes the end of the program'''
    lbp = 0

if __name__ == "__main__":
    assert parse("1+2") == 3
    assert parse("2*3") == 6
    assert parse("3-2") == 1
    assert parse("10/2") == 5
    assert parse("1 + 2 * 3") == 7
    assert parse("2 - 4/2") == 0
    print "Done."