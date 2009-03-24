'''Externally defined basic operators for arithmetic operations'''

from zope import interface
import grokcore.component as grok
from calculator.plugins.interfaces import IOperator
from calculator import expression

class operator_mod_token(grok.GlobalUtility):
    interface.implements(IOperator)
    grok.name('%')
    lbp = 10
    def nud(self):
        return expression(100)
    def led(self, left):
        return left % expression(10)
