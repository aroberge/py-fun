# This is an example using the Zope Component Architecture for plugins
# Since the expression hack doesn't work with ZCA (you would have two 
# module paths for some expressions, and that wouldn't work) we have
# moved the main calculator file into a package.

from calculator import calculate

assert calculate("+1") == 1
assert calculate("-1") == -1
assert calculate("10") == 10
assert calculate("1+2") == 3
assert calculate("1+2+3") == 6
assert calculate("1+2-3") == 0
assert calculate("1+2*3") == 7
assert calculate("1*2+3") == 5
assert calculate("6*2/3") == 4

# "**" has not been activated at the start in base.py
try:
    assert calculate("2**3") == 8
    raise "** should not have been activated!"
except SyntaxError:
    print "Correcting error..."
    import calculator.plugins.op_2
assert calculate("2*2**3") == 16

# Unregistering in runtime is an unusual use case, but possible:
from zope import component
from calculator.plugins.interfaces import IOperator
plus = component.getUtility(IOperator, '+')
from zope.component import getGlobalSiteManager
gsm = getGlobalSiteManager()
gsm.unregisterUtility(plus, name='+')

try:
    assert calculate("1+2") == 3
    raise "Deactivation failed!"
except SyntaxError:
    gsm.registerUtility(plus, name='+')
assert calculate("1+2") == 3

# Simulating dynamic external plugin initialization
# With the CA it's exactly the same as normal activation.
import external.op_3
assert calculate("7%2") == 1

print "Done!"
