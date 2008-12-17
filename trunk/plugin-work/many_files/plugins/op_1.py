'''Externally defined basic operators for arithmetic operations'''

# Note that "expression" is an object defined globally via indirect means.

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