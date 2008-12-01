"""Plugin for loading and transforming ReST files."""

# Note: much of the rst directives code was created as part of the
# Google Highly Open Participation Contest 2007/8 by
# Copyright (C) 2008 Zachary Voase <cracka80 at gmail dot com>
#
# It was adapted and incorporated into Crunchy by A. Roberge
# and modified for this version.

# All plugins should import the crunchy plugin API via interface.py


from os import linesep
from docutils.parsers import rst
from docutils.writers.html4css1 import HTMLTranslator
from docutils import nodes

def int_or_one(argument):
    """If no argument is present, returns 1.
    Else returns argument as integer."""
    if argument and argument.strip():
        return int(argument)
    else:
        return 1

class pre(nodes.raw):
    def __init__(self, *args, **kwargs):
        nodes.raw.__init__(self, *args, **kwargs)
        self.tagname = "pre"

class InterpreterDirective(rst.Directive):
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'linenumber' : int_or_one,
        'log_id' : str
    }
    has_content = True
    def run(self):
        code = linesep.join(self.content)
        if self.arguments[0].strip() not in ['interpreter', 'isolated',
                                    'parrot', 'Parrots', 'TypeInfoConsole']:
            raise ValueError("Wrong interpreter type: %s" % (self.arguments[0].strip(),))
        listOut = [ x.strip() for x in self.arguments ]
        for key in [ "linenumber", "log_id" ]:
            if self.options.has_key(key):
                listOut.append(key + "=%s" % (str(self.options[key]),))
        titleAttr = " ".join(listOut)
        return [ pre(title=titleAttr, text=code) ]

class EditorDirective(rst.Directive):
    required_arguments = 0
    optional_arguments = 5
    final_argument_whitespace = False
    option_spec = {
        'linenumber' : int_or_one,
        'log_id' : str
    }
    has_content = True
    def run(self):
        code = linesep.join(self.content)
        for arg in self.arguments:
            if arg.strip() not in ['no_copy', 'no_pre',
                                   'external', 'no_internal']:
                raise ValueError("Invalid argument: %s" % (arg.strip(),))
        listOut = [ x.strip() for x in ['editor'] + self.arguments ]
        for key in [ "linenumber", "log_id" ]:
            if self.options.has_key(key):
                listOut.append(key + "=%s" % (str(self.options[key]),))
        titleAttr = " ".join(listOut)
        return [ pre(title=titleAttr, text=code) ]

class DocTestDirective(rst.Directive):
    required_arguments = 0
    optional_arguments = 1
    option_spec = {
        'linenumber' : int_or_one,
        'log_id' : str
    }
    has_content = True
    def run(self):
        self.assert_has_content()
        code = linesep.join(self.content)
        listOut = [ x.strip() for x in ['doctest'] + self.arguments ]
        for key in [ "linenumber", "log_id" ]:
            if self.options.has_key(key):
                listOut.append(key + "=%s" % (str(self.options[key]),))
        titleAttr = " ".join(listOut)
        return [ pre(title=titleAttr, text=code) ]

class PythonCodeDirective(rst.Directive):
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        'linenumber' : int_or_one
    }
    has_content = True
    def run(self):
        code = linesep.join(self.content)
        listOut = ['python_code']
        if self.options.has_key("linenumber"):
            listOut.append("linenumber=%d" % (self.options["linenumber"],))
        titleAttr = " ".join(listOut)
        return [ pre(title=titleAttr, text=code) ]

class NoVLAMDirective(rst.Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}
    has_content = True
    def run(self):
        self.assert_has_content()
        code = linesep.join(self.content)
        listOut = ['no_vlam']
        titleAttr = " ".join(listOut)
        return [ pre(title=titleAttr, text=code) ]

DIRECTIVE_DICT = {
    'interpreter' : InterpreterDirective,
    'editor' : EditorDirective,
    'doctest' : DocTestDirective,
    'py_code' : PythonCodeDirective,
    'python_code' : PythonCodeDirective,
    'no_vlam' : NoVLAMDirective
    }

def visit_pre(translator, node):
    attrDict = {}
    for key, value in node.attributes.items():
        if value and (key is not "xml:space"):
            attrDict[key] = value
    translator.body.append(translator.starttag(node, 'pre', **attrDict))

def depart_pre(translator, node):
    translator.body.append('\n</pre>\n')

HTMLTranslator.visit_pre = visit_pre
HTMLTranslator.depart_pre = depart_pre

for key, value in DIRECTIVE_DICT.items():
    rst.directives.register_directive( key, value )

#class ReST_file(object):
#    """Represents file with transformed text from rst into html.
#    vlam thinks it is an ordinary file object"""
#    def __init__(self, data):
#        self._data = data
#    def read(self):
#        return self._data
#
#def load_rst(request):
#    """Loads rst file from disk,
#    transforms it into html and then creates new page"""
#    url = request.args["url"]
#    file_ = open(url)
#
#    rst_file = ReST_file(publish_string(file_.read(), writer_name="html"))
#    page = plugin['create_vlam_page'](rst_file, url, local=True,
#                                      username=request.crunchy_username)
#
#    request.send_response(200)
#    request.end_headers()
#    request.wfile.write(page.read())
#
#def convert_rst(path, local=True):
#    '''converts an rst file into a proper crunchy-ready html page'''
#    if local:
#        file_ = open(path)
#    else:
#        file_ = urlopen(path)
#    rst_file = ReST_file(publish_string(file_.read(), writer_name="html"))
#    return rst_file
#
#def insert_load_rst(page, elem, uid):
#    "Inserts a javascript browser object to load a local reStructuredText file."
#    plugin['services'].insert_file_tree(page, elem, uid, '/jquery_file_tree_rst',
#                                '/rst', 'Load local reStructuredText file', 'Load rst file')
#    return
#
#def filter_rst(filename, basepath):
#    '''filters out all files and directory with filename so as to include
#       only files whose extensions are ".rst" or ".txt" with the possible
#       exception of ".crunchy" - the usual crunchy default directory.
#    '''
#    if filename.startswith('.') and filename != ".crunchy":
#        return True
#    else:
#        fullpath = os.path.join(basepath, filename)
#        if os.path.isdir(fullpath):
#            return False   # do not filter out directories
#        ext = os.path.splitext(filename)[1][1:] # get .ext and remove dot
#        if ext == 'rst' or ext == "txt":
#            return False
#        else:
#            return True
#
#def jquery_file_tree_rst(request):
#    '''extract the file information and formats it in the form expected
#       by the jquery FileTree plugin, but excludes some normally hidden
#       files or directories, to include only reStructuredText files.'''
#    plugin['services'].filtered_dir(request, filter_rst)
#    return
