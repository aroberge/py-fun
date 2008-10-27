'''
This module contains the base _parser class from which all parsers should be
derived.   Some methods are implemented only to provide testing, and
are meant to be overriden.

Note: by convention, the name of the parser class is identical to the name of
the module.  To avoid problems on different platforms, all class names
will use lowercase letters only.

The name of the parser will also be used as the docpicture label as in:
..docpicture:: _parser

'''

import re
import src.svg as svg

''' So as to make the parser classes more readable, we suggest that
statement patterns, if using the re module, or the grammar definition,
if using some other module, as well as svg "defs" be defined first,
before the class definition.'''

# To enable testing, we define at least one pattern to match.
_patterns = {
    # anything with "good" in it is declared to be good ;-)
    'good': re.compile(".*good.*")
}



class BaseParser(object):
    '''Base class for all the parsers'''
    def __init__(self):
        self.patterns = _patterns  # definitely needs to be overriden!

    def svg_defs(self):
        '''default svg_defs; normally overriden by parsers'''
        defs = svg.SvgDefs()
        defs.append(svg.Comment("For testing purpose"))
        return defs

    def parse_single_line(self, line):
        '''Parses a given line to see if it match a known pattern'''
        line = line.strip()
        for name in self.patterns:
            result = self.patterns[name].match(line)
            if result is not None:
                return name, result.groups()
        return None, line

    def parse_lines_of_code(self, lines):
        '''Parses all received lines of code.

           If errors are found, returns a list of line with errors and an
           empty string, otherwise returns None (for no error) and a list of
           lines parsed to extract the relevant information.
        '''
        ok_lines = []
        problem_lines = []
        for line in lines:
            if line.strip() == "":
                continue
            result = self.parse_single_line(line)
            if result[0] == None:
                problem_lines.append(line)
            else:
                ok_lines.append(result)
        if problem_lines:
            return problem_lines, self.draw(ok_lines)
        else:
            return None, self.draw(ok_lines)

    def draw(self, lines):
        '''fake function; normally would convert parsed lines of code
           into svg drawing statements'''
        new_lines = [str(line) for line in lines]
        return "<pre>Drawing: " + "\nDrawing: ".join(new_lines) + "</pre>"
