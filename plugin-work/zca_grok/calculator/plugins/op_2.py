'''Externally defined "advanced" operator for arithmetic operations'''

from zope import interface
import grokcore.component as grok
from interfaces import IOperator
from calculator import expression

class operator_pow_token(grok.GlobalUtility):
    grok.implements(IOperator)
    grok.name('**')
    lbp = 30
    def led(self, left):
        return left ** expression(30-1)