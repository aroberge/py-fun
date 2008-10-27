'''

docpicture

Need to explain what it does here
'''
import re
import src.svg as svg
import src.parsers_loader
import src.server

docpicture_directive_pattern = re.compile("\s*\.\.docpicture::\s*(.+?)$")

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
            .warning{color: red;}"""

    def reset(self):
        '''resets (or sets) values to initial choices needed to process
        a new document'''
        self.indentation = None
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
            return False
        else:
            self.indentation = line.index("..docpicture")
            parser_name = result.groups()[0]
            if parser_name in self.parsers:
                self.current_parser_name = result.groups()[0]
                return True
            else:
                return False

    def is_docpicture_code(self, line):
        '''return True if the indentation (number of spaces at the beginning
           of a line) is greater than the given indentation, False otherwise,
           with the exception that blank lines are considered always have
           the indentation required to be part of the docpicture code.
        '''
        if len(line.strip()) == 0:
            return True
        if line.startswith(" "*(self.indentation+1)):
            return True
        else:
            return False

    def process_docpicture_code(self, lines):
        ''' feeds a list of lines to the appropriate docpicture parser'''
        return self.parsers[self.current_parser_name].parse_lines_of_code(lines)

    def embed_docpicture_code(self, lines):
        '''includes the docpicture lines of code in the document, as well as
        any lines found to have syntax errors by the parser, followed by
        the drawing itself (preceded by svg defs, if not done previously).'''
        pre = svg.XmlElement("pre", text="\n".join(lines))
        pre.attributes["class"] = "docpicture"
        self.body.append(pre)
        # exclude the docpicture directive from the call
        flag, drawing = self.process_docpicture_code(lines[1:])
        if flag is not None:
            text = "WARNING: unrecognized syntax\n" + "\n".join(flag)
            pre = svg.XmlElement("pre", text=text)
            pre.attributes["class"] = "warning"
            self.body.append(pre)
        if self.current_parser_name not in self.included_defs:
            self.included_defs.append(self.current_parser_name)
            self.body.append(self.parsers[self.current_parser_name].svg_defs())
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
                    docpicture_lines.append(line)
            else:
                if self.is_docpicture_code(line):
                    docpicture_lines.append(line)
                else:
                    self.embed_docpicture_code(docpicture_lines)
                    self.current_parser_name = None
                    docpicture_lines = []
                    new_lines.append(line)
        # we have to take care of the last bunch of unprocessed lines
        if new_lines:
            text = "\n".join(new_lines)
            self.body.append(svg.XmlElement("pre", text=text))
        elif docpicture_lines:
            self.embed_docpicture_code(docpicture_lines)
        return

def get_docstring(obj):
    '''gets the docstring corresponding to a given object'''
    try:
        doc = obj.__doc__
    except:
        doc = None
    try:
        name = repr(obj.__name__)
    except:
        name = "Unknown"
    if doc is None:
        doc = "No docstring is available for this object: %s" % name
    print doc
    return doc

def view(obj):
    import sys, time
    print "Server will be active for 10 seconds; try reloading the page"
    src.parsers_loader.load_parsers()
    xml_doc = DocpictureDocument(src.parsers_loader.PARSERS)
    xml_doc.create_document(get_docstring(obj))
    test_doc = src.server.Document(str(xml_doc.document))
    threaded_server = src.server.ServerInThread()
    threaded_server.start()
    colors = ['red', 'green', 'yellow', 'brown', 'blue', 'magenta', 'cyan',
              'tan', 'white', 'black', 'red']

    for i in range(10, 0, -1):
        print i,
        sys.stdout.flush()
        time.sleep(1)

    src.server.stop_server(threaded_server.port)
    print "Done!"


if __name__ == "__main__":
    import fake_turtle
    view(fake_turtle)