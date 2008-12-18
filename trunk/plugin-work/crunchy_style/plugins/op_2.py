'''Externally defined "advanced" operator for arithmetic operations'''

def register(OPERATORS):
    OPERATORS['**'] = operator_pow_token

class operator_pow_token(object):
    lbp = 30
    def led(self, left):
        return left ** expression(30-1)