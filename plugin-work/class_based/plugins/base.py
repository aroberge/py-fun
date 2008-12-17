'''Simple class based plugin system

Inspired by the tutorial at
http://lucumr.pocoo.org/blogarchive/python-plugin-system

'''

import os
import sys

OPERATORS = {}

class Plugin(object):
    pass

def init_plugins(expression):
    '''simple plugin initializer
    '''
    find_plugins(expression)
    register_plugins()

def find_plugins(expression):
    '''find all files in the plugin directory and imports them'''
    plugin_dir = (os.path.dirname(os.path.realpath(__file__)))
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
        OPERATORS[plugin.symbol] = plugin
