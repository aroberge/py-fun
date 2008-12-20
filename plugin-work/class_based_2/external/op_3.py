'''Externally defined basic operators for arithmetic operations'''

from plugins.base import Plugin

class operator_mod_token(Plugin):
    symbol = '%'
    lbp = 10
    def nud(self):
        return expression(100)
    def led(self, left):
        return left % expression(10)
