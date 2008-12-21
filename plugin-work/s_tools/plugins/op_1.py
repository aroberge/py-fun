'''Externally defined basic operators for arithmetic operations'''

from plugins.base import Plugin

class operator_add_token(Plugin):
    symbol = '+'
    lbp = 10
    def nud(self):
        return self.expression(100)
    def led(self, left):
        return left + self.expression(10)

class operator_sub_token(Plugin):
    symbol = '-'
    lbp = 10
    def nud(self):
        return -self.expression(100)
    def led(self, left):
        return left - self.expression(10)

class operator_mul_token(Plugin):
    symbol = '*'
    lbp = 20
    def led(self, left):
        return left * self.expression(20)

class operator_div_token(Plugin):
    symbol = '/'
    lbp = 20
    def led(self, left):
        return left / self.expression(20)