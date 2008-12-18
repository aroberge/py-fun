'''Simple class based plugin system

Inspired by the approach used by Crunchy.

'''

import os
import sys

OPERATORS = {}

class Plugin(object):
    pass

def init_plugins(expression):
    '''simple plugin initializer

        find all files in the plugin directory, import them and
        register those that are plugins.
    '''
    plugin_dir = (os.path.dirname(os.path.realpath(__file__)))
    plugin_files = [x[:-3] for x in os.listdir(plugin_dir) if x.endswith(".py")]
    sys.path.insert(0, plugin_dir)
    for plugin in plugin_files:
        mod = __import__(plugin)
        if hasattr(mod, "register"):
            mod.expression = expression
            mod.register(OPERATORS)
