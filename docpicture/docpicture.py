'''

docpicture

Need to explain what it does here
'''
import pydoc
from StringIO import StringIO
import re
import sys

import src.svg as svg
import src.parsers_loader
import src.server

docpicture_directive_pattern = re.compile("^\s*\.\.docpicture::\s*(.+?)$")
# note: sometimes, the Python help display code indented with a string like:
# "    |   ".
indented_d_pattern = re.compile("^\s*\|\s*\.\.docpicture::\s*(.+?)$")

class DocpictureDocument(object):
    '''
    A DocpictureDocument is an xml document that can contain svg images.

    It is usually created from a Python docstring that contains some
    "docpicture directives".

    '''
    def __init__(self, parsers=None):
        if parsers is None:
            self.parsers = {}
        else:
            self.parsers = parsers
        self.reset()
        self.style = """p{width:800px;}
            pre{font-size: 12pt;}
            .docpicture{color: blue;}
            .warning{color: red;}
            .bold{font-weight:bold; color:darkblue;}
            """

    def reset(self):
        '''resets (or sets) values to initial choices needed to process
        a new document'''
        self.indentation = None
        self.vertical_bar_indentation = False
        self.current_parser_name = None
        self.included_defs = []

    def is_docpicture_directive(self, line):
        """ Identifies if a line corresponds to a docpicture directives.

            If it is a docpicture directive, it returns the indentation (number of
            spaces at the beginning of the line) and the name of the processor
            if it is a known processor; otherwise it returns False.
        """
        result = docpicture_directive_pattern.search(line.rstrip())
        if result is None:
            result = indented_d_pattern.search(line.rstrip())
            if result is None:
                return False
            else:  # line start with something like "     |   "
                self.vertical_bar_indentation = True

        parser_name = result.groups()[0]
        if parser_name in self.parsers:
            self.current_parser_name = result.groups()[0]
            self.indentation = line.index("..docpicture")
            return True
        else:
            return False

    def is_docpicture_code(self, line):
        '''return True if the indentation (number of spaces at the beginning
           of a line) is greater than the given indentation, False otherwise,
           with the exception that blank lines are considered always have
           the indentation required to be part of the docpicture code.
        '''
        if self.vertical_bar_indentation:
            line = line.replace(" | ", "   ", 1)
        if len(line.strip()) == 0:
            return True
        if line.startswith(" "*(self.indentation+1)):
            return True
        else:
            return False

    def process_docpicture_code(self, lines):
        ''' feeds a list of lines to the appropriate docpicture parser
        and some svg (or other xml) instructions for including the
        corresponding drawing.'''
        return self.parsers[self.current_parser_name].create_drawing(lines)

    def embed_docpicture_code(self, lines):
        '''includes the docpicture lines of code in the document, as well as
        any lines found to have syntax errors by the parser, followed by
        the drawing itself (preceded by svg defs, if not done previously).'''
        pre = svg.XmlElement("pre", text="\n".join(lines))
        pre.attributes["class"] = "docpicture"
        self.body.append(pre)
        if len(lines) == 1:  # missing code!
            text = "WARNING: Missing code for this docpicture.\n"
            pre = svg.XmlElement("pre", text=text)
            pre.attributes["class"] = "warning"
            self.body.append(pre)
            return
        # exclude the docpicture directive from the call
        flag, drawing = self.process_docpicture_code(lines[1:])
        if flag is not None:
            text = "WARNING: unrecognized syntax\n" + "\n".join(flag)
            pre = svg.XmlElement("pre", text=text)
            pre.attributes["class"] = "warning"
            self.body.append(pre)
        if self.current_parser_name not in self.included_defs:
            self.included_defs.append(self.current_parser_name)
            self.body.append(self.parsers[self.current_parser_name].get_svg_defs())
        self.body.append(drawing)
        return

    def create_document(self, text):
        '''creates an xml document from a text given as a series of lines,
        possibly with embedded docpicture directives.'''
        self.document = svg.XmlDocument()
        self.head = self.document.head
        self.body = self.document.body
        self.head.append(svg.XmlElement("style", text=self.style))
        lines = text.split("\n")
        self.process_lines_of_text(lines)
        return

    def process_lines_of_text(self, lines):
        '''processes some text passed as a series of lines,
        to embed docpictures where appropriate.  The lines are expected
        NOT to end with a new line character.

        Appends the processed text inside the document body.'''
        self.reset()
        new_lines = []
        docpicture_lines = []
        for line in lines:
            if len(line) > 0:
                assert line[-1] != "\n"
            if self.current_parser_name is None:
                if not self.is_docpicture_directive(line):
                    new_lines.append(line)
                else:
                    # self.current_parser_name will have been set by
                    # self.is_docpicture_directive
                    text = '\n'.join(new_lines)
                    new_lines = []
                    self.body.append(svg.XmlElement("pre", text=text))
                    if self.vertical_bar_indentation:
                        line = line.replace(" | ", "   ", 1)
                    docpicture_lines.append(line)
            else:
                if self.is_docpicture_code(line):
                    if self.vertical_bar_indentation:
                        line = line.replace(" | ", "   ", 1)
                    docpicture_lines.append(line)
                else:
                    self.embed_docpicture_code(docpicture_lines)
                    docpicture_lines = []
                    if not self.is_docpicture_directive(line):
                        new_lines.append(line)
                        self.current_parser_name = None
                    else:  # two docpicture directives in a row
                        if self.vertical_bar_indentation:
                            line = line.replace(" | ", "   ", 1)
                        docpicture_lines.append(line)

        # we have to take care of the last bunch of unprocessed lines
        if new_lines:
            text = "\n".join(new_lines)
            self.body.append(svg.XmlElement("pre", text=text))
        elif docpicture_lines:
            self.embed_docpicture_code(docpicture_lines)
        return


    def find_object(self, obj, attr):
        '''given an object "obj", attempts to find an attribute
        in the module where obj is located, or an attribute of the
        module if obj is a module'''
        try:
            return getattr(obj, attr)
        except:
            try:
                return getattr(sys.modules[obj.__module__], attr)
            except:
                return False

def my_help(obj):
    _io = StringIO()
    def my_pager(text):
        _io.write(pydoc.plain(text))
        return
    def bold(self, text):
        return "<span class='bold'>%s</span>"%text
    #
    saved_pager = pydoc.pager
    saved_bold = pydoc.TextDoc.bold
    pydoc.pager = my_pager
    pydoc.TextDoc.bold = bold
    #
    pydoc.help(obj)
    _help = _io.getvalue()
    _io.close()
    pydoc.pager = saved_pager
    pydoc.TextDoc.bold = saved_bold
    return _help


threaded_server = None
def view(obj):
    global threaded_server
    if not src.parsers_loader.PARSERS:
        src.parsers_loader.load_parsers()
    xml_doc = DocpictureDocument(src.parsers_loader.PARSERS)
    xml_doc.create_document(my_help(obj))

    dummy = src.server.Document(str(xml_doc.document))
    if threaded_server is None:
        threaded_server = src.server.ServerInThread()
        threaded_server.start()
    else:
        print "Use the reload button of your web browser to see the new display."

def stop_server():
    global threaded_server
    src.server.stop_server(threaded_server.port)
    del threaded_server
    threaded_server = None
    print "Server shut down!"


if __name__ == "__main__":
    import fake_turtle
    view(fake_turtle)
    dummy = raw_input("Press any key to end.")
    stop_server()