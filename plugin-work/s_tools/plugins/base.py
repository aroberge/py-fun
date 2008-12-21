'''setuptools based plugin system.

Inspired by the tutorial at
http://lucumr.pocoo.org/blogarchive/setuptools-plugins
and the similar one at
http://base-art.net/Articles/64/

'''
import os
import sys
import pkg_resources  # setuptools specific

OPERATORS = {}
ENTRYPOINT = 'plugin_tutorial.s_tools'  # same name as in setup.py
PLUGIN_DIR = os.path.dirname(os.path.realpath(__file__))

class Plugin(object):
    '''A Borg class.
    '''
    _shared_states = {}
    def __init__(self):
        self.__dict__ = self._shared_states

def init_plugins(expression):
    '''simple plugin initializer
    '''
    Plugin().expression = expression  # fixing the wart
    load_plugins()

def load_plugins():
    '''setuptools based plugin loader'''
    for entrypoint in pkg_resources.iter_entry_points(ENTRYPOINT):
        plugin_class = entrypoint.load()
        OPERATORS[plugin_class.symbol] = plugin_class
