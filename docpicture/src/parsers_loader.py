"""
This module loads parsers

"""

import sys
import os
import os.path

PARSERS = {}

def register_parser(klass):
    instance = klass()
    PARSERS[instance.directive_name] = klass()

def gen_parsers_list(parser_dir):
    '''looks for all python files in the specified directory.'''
    try:
        parser_files = [x[:-3] for x in os.listdir(parser_dir) if x.endswith(".py")]
    except OSError:
        print "Can not find the parser files; parser path =", parser_dir
        parser_files = []
    return parser_files

def load_parsers(testing=False):
    """load the parsers and has them self-register."""

    base_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                               ".."))
    sys.path.insert(0, base_dir)
    parser_dir = os.path.join(base_dir, "parsers")
    sys.path.insert(0, parser_dir)
    parsers = gen_parsers_list(parser_dir)
    imported_parsers = []
    os.chdir(parser_dir)

    for parser in parsers:
        mod = __import__ (parser, globals())
        imported_parsers.append(mod)

    for mod in imported_parsers:
        if hasattr(mod, "register_docpicture_parser"):
            if not testing:
                mod.register_docpicture_parser(register_parser)
            else:
                print "Parser found:", mod.__name__
        elif testing:
            print "Non-parser Python file found:", mod.__name__
    print PARSERS

if __name__ == "__main__":
    load_parsers(testing=True)