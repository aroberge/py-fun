# This is an example using the Zope Component Architecture for plugins
# Since the expression hack doesn't work with ZCA (you would have two 
# module paths for some expressions, and that wouldn't work) we have
# moved the main calculator file into a package.

import calculator
from zope.configuration import xmlconfig
xmlconfig.file('configure.zcml', package=calculator)

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

# There is not much runtime activation/deactivation in Grok, but you can use the
# plain ZCA techniques for this, see plain_zca.
assert calculate("2*2**3") == 16

# But we can activate/load new packages at least:
import external
from zope.configuration import xmlconfig
xmlconfig.file('configure.zcml', package=external)

assert calculate("7%2") == 1

print "Done!"
