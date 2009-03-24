'''Externally defined basic operators for arithmetic operations'''

from zope import interface, component
from interfaces import IOperator
from calculator import expression

class operator_add_token(object):
    interface.implements(IOperator)
    lbp = 10
    def nud(self):
        return expression(100)
    def led(self, left):
        return left + expression(10)
component.provideUtility(operator_add_token(), name='+')

class operator_sub_token(object):
    interface.implements(IOperator)
    lbp = 10
    def nud(self):
        return -expression(100)
    def led(self, left):
        return left - expression(10)
component.provideUtility(operator_sub_token(), name='-')

class operator_mul_token(object):
    interface.implements(IOperator)
    lbp = 20
    def led(self, left):
        return left * expression(20)
component.provideUtility(operator_mul_token(), name='*')

class operator_div_token(object):
    interface.implements(IOperator)
    lbp = 20
    def led(self, left):
        return left / expression(20)
component.provideUtility(operator_div_token(), name='/')
