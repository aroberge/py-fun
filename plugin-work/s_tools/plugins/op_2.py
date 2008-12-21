'''Externally defined "advanced" operator for arithmetic operations'''

from plugins.base import Plugin

class operator_pow_token(Plugin):
    symbol = '**'
    lbp = 30
    def led(self, left):
        return left ** self.expression(30-1)