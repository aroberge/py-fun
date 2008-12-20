'''Simple class based plugin system with activation/desactivation
'''

import os
import sys

OPERATORS = {}

# We simulate a configuration file that would be based on a user's preference
# as to which plugin should be activated by default
# We will leave one symbol "**" out of the list as a test.
preferences = ['+', '-', '*', '/']

# We also keep track of all available plugins
all_plugins = {}

class Plugin(object):
    '''base class for all plugins'''

    def activate(self):
        '''activate a given plugin'''
        OPERATORS[self.symbol] = self.__class__
        if self.symbol not in all_plugins:
            all_plugins[self.symbol] = self.__class__

    def desactivate(self):
        '''desactivate a given plugin'''
        if self.symbol in OPERATORS:
            del OPERATORS[self.symbol]

def activate(symbol):
    '''activate a given plugin based on its symbol'''
    if symbol in OPERATORS:
        return
    all_plugins[symbol]().activate()

def desactivate(symbol):
    '''desactivate a given plugin, based on its symbol'''
    if symbol not in OPERATORS:
        return
    all_plugins[symbol]().desactivate()


def init_plugins(expression):
    '''simple plugin initializer
    '''
    find_plugins(expression)
    register_plugins()

def find_plugins(expression):
    '''find all files in the plugin directory and imports them'''
    plugin_dir = os.path.dirname(os.path.realpath(__file__))
    plugin_files = [x[:-3] for x in os.listdir(plugin_dir) if x.endswith(".py")]
    sys.path.insert(0, plugin_dir)
    for plugin in plugin_files:
        mod = __import__(plugin)
        mod.expression = expression

def register_plugins():
    '''Register all class based plugins.

       Uses the fact that a class knows about all of its subclasses
       to automatically initialize the relevant plugins
    '''
    for plugin in Plugin.__subclasses__():
        # only register plugins according to user's preferences
        if plugin.symbol in preferences:
            plugin().activate()
        else:   # record its existence
            all_plugins[plugin.symbol] = plugin
