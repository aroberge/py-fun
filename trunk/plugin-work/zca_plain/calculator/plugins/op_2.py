'''Externally defined "advanced" operator for arithmetic operations'''

from zope import interface, component
from interfaces import IOperator
from calculator import expression

class operator_pow_token(object):
    interface.implements(IOperator)
    lbp = 30
    def led(self, left):
        return left ** expression(30-1)
component.provideUtility(operator_pow_token(), name='**')
