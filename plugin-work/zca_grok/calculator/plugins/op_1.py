'''Externally defined basic operators for arithmetic operations'''

from zope import interface
import grokcore.component as grok
from interfaces import IOperator
from calculator import expression

class operator_add_token(grok.GlobalUtility):
    grok.implements(IOperator)
    grok.name('+')
    lbp = 10
    def nud(self):
        return expression(100)
    def led(self, left):
        return left + expression(10)

class operator_sub_token(grok.GlobalUtility):
    grok.implements(IOperator)
    grok.name('-')
    lbp = 10
    def nud(self):
        return -expression(100)
    def led(self, left):
        return left - expression(10)

class operator_mul_token(grok.GlobalUtility):
    grok.implements(IOperator)
    grok.name('*')
    lbp = 20
    def led(self, left):
        return left * expression(20)

class operator_div_token(grok.GlobalUtility):
    grok.implements(IOperator)
    grok.name('/')
    lbp = 20
    def led(self, left):
        return left / expression(20)
