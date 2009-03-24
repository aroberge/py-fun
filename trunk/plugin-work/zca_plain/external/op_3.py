'''Externally defined basic operators for arithmetic operations'''

from zope import interface, component
from calculator.plugins.interfaces import IOperator
from calculator import expression

class operator_mod_token(object):
    interface.implements(IOperator)
    lbp = 10
    def nud(self):
        return expression(100)
    def led(self, left):
        return left % expression(10)
component.provideUtility(operator_mod_token(), name='%')
