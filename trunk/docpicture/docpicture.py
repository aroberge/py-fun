'''

docpicture

Need to explain what it does here
'''


import re
import src.svg as svg
import src.parsers_loader

BEGIN_DOCUMENT = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html
    PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:svg="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink">
  <head>
    <style>
        p{width:800px;}
        pre{font-size: 12pt;}
        .docpicture{color: blue;}
        .warning{color: red;}
    </style>
  </head>
<body>"""

END_DOCUMENT = "</body></html>"

parsers = {}
parsers_defs = {}

#def view(obj):
#    """
#    Allows viewing docstring with embedded images.
#
#    To see a normal docstring, use help(object).
#    To see a docstring with embedded images, use docpicture.view(object).
#    It is assumed that the images are included (encoded in base 64) in
#    your Python module.
#
#    The result will be an html file displayed in your default browser,
#    with the images inserted.
#
#    For example: docpicture = python_powered_w.png
#
#    Limitation: the filename must be a valid Python identifier.
#    Note that this works with gif images  docpicture=python_g.gif
#
#    as well as jpeg images docpicture = python_j.jpg
#
#    All that is required is for the filename (without the extension) be a
#    unique value.  Note that the same image can appear twice.
#
#    docpicture = python_powered_w.png
#    """
#    source_module = sys.modules[obj.__module__]
#
#    docpicture_pattern = re.compile("\s*(docpicture\s*=\s*.+?)\s")
#    image_name_pattern = re.compile("\s*docpicture\s*=\s*(.+?)\s")
#
#    docstring = obj.__doc__
#    image_filename = image_name_pattern.search(obj.__doc__)
#    while image_filename is not None:
#        filename = image_filename.groups()[0]
#        base_name, ext = filename.split('.')
#        image = getattr(source_module, base_name).decode("base64")
#
#        image_file = open(filename, "wb")
#        image_file.write(image)
#        image_file.close()
#        docstring = docpicture_pattern.sub("</pre><img src=%s><pre>" % filename,
#                                    docstring, count=1)
#        image_filename = image_name_pattern.search(docstring)
#
#    html_file = open("test.html", 'w')
#    html_file.write(html_template % docstring)
#    html_file.close()
#    url = os.path.join(os.getcwd(), "test.html")
#    webbrowser.open(url)

docpicture_directive_pattern = re.compile("\s*\.\.docpicture::\s*(.+?)$")
#def identify_docpicture_directive(line):
#    """ Identifies if a line corresponds to a docpicture directives.
#
#        If it is a docpicture directive, it returns the indentation (number of
#        spaces at the beginning of the line) and the name of the processor;
#        otherwise it returns None.
#    """
#    result = docpicture_directive_pattern.search(line.rstrip())
#    if result is None:
#        return None
#    else:
#        return line.index("..docpicture"), result.groups()[0]

def is_code(line, indentation):
    '''return True if the indentation (number of spaces at the beginning
       of a line) is greater than the given indentation, False otherwise,
       with the exception that blank lines are considered to be part of the code.
    '''
    if len(line.strip()) == 0:
        return True
    if line.startswith(" "*(indentation+1)):
        return True
    else:
        return False

def parse_code(parser, code):
    '''Calls the appropriate parser, based on its name, to produce the
    svg diagram corresponding to the code.'''
    try:
        return parsers[parser](code)
    except KeyError:
        return "<pre class='warning'>Unknown parser %s.</pre>" % parser, None

def parse_document(text):
    '''parses an entire document, received as a string, and outputs
    an html document with svg code inserted by the appropriate parser.
    The original text is inserted into some pre-formatted sections,
    so as to retain the original look - including any existing ascii diagrams.
    '''
    lines = text.split("\n")
    new_lines = [BEGIN_DOCUMENT, "<pre>\n"]
    included_defs = []
    parsers_used = []
    indentation = None
    current_parser = None
    current_defs = None
    lines_of_code = None
    for line in lines:
        if lines_of_code is not None: # we're inside docpicture code
            if is_code(line, indentation):  # still inside
                new_lines.append(line)
                lines_of_code.append(line)
            else:                           # back to regular help
                new_lines.append("</pre>")
                if current_defs is not None:  # need to rewrite this
                    new_lines.append(current_defs)
                    current_defs = None
                append_parser_result(new_lines, current_parser, lines_of_code)
                new_lines.append("<pre>\n"+line)
                lines_of_code = None
                current_parser = indentation = None
        else:
            parsing_call = identify_docpicture_directive(line)
            if parsing_call is not None:
                indentation, current_parser = parsing_call
                if current_parser not in parsers_used:
                    parsers_used.append(current_parser)
                    try:
                        current_defs = parsers_defs[current_parser]()
                        included_defs.append(current_defs)
                    except KeyError:
                        pass
                lines_of_code = []
                new_lines.append("</pre>\n<pre class='docpicture'>")
            new_lines.append(line)
    # We have to guard against the situation where we ended with a docpicture
    if lines_of_code is not None:
        new_lines.append("</pre>")
        append_parser_result(new_lines, current_parser, lines_of_code)
        new_lines.append(END_DOCUMENT)
    else:
        new_lines.append("</pre>\n"+END_DOCUMENT)
    return "\n".join(new_lines)


def create_document(text):
    '''parses a docstring, and outputs
    an html document with svg code inserted by the appropriate parser.
    The original text is inserted into some pre-formatted sections,
    so as to retain the original look - including any existing ascii diagrams.
    '''
    lines = text.split("\n")
    new_lines = [BEGIN_DOCUMENT, "<pre>\n"]
    included_defs = []
    parsers_used = []
    indentation = None
    current_parser = None
    current_defs = None
    lines_of_code = None
    for line in lines:
        if lines_of_code is not None: # we're inside docpicture code
            if is_code(line, indentation):  # still inside
                new_lines.append(line)
                lines_of_code.append(line)
            else:                           # back to regular help
                new_lines.append("</pre>")
                if current_defs is not None:  # need to rewrite this
                    new_lines.append(current_defs)
                    current_defs = None
                append_parser_result(new_lines, current_parser, lines_of_code)
                new_lines.append("<pre>\n"+line)
                lines_of_code = None
                current_parser = indentation = None
        else:
            parsing_call = identify_docpicture_directive(line)
            if parsing_call is not None:
                indentation, current_parser = parsing_call
                if current_parser not in parsers_used:
                    parsers_used.append(current_parser)
                    try:
                        current_defs = parsers_defs[current_parser]()
                        included_defs.append(current_defs)
                    except KeyError:
                        pass
                lines_of_code = []
                new_lines.append("</pre>\n<pre class='docpicture'>")
            new_lines.append(line)
    # We have to guard against the situation where we ended with a docpicture
    if lines_of_code is not None:
        new_lines.append("</pre>")
        append_parser_result(new_lines, current_parser, lines_of_code)
        new_lines.append(END_DOCUMENT)
    else:
        new_lines.append("</pre>\n"+END_DOCUMENT)
    return "\n".join(new_lines)

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
            spaces at the beginning of the line) and the name of the processor;
            otherwise it returns False.
        """
        result = docpicture_directive_pattern.search(line.rstrip())
        if result is None:
            return False
        else:
            self.indentation = line.index("..docpicture")
            self.current_parser_name = result.groups()[0]
            return True

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
            pre = svg.XmlElement("pre", text="\n".join(flag))
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
        self.process_text(lines)

    def process_lines_of_text(self, lines):


        return True

        new_lines = []
        docpicture_lines = []
        for line in lines:
            if self.current_parser_name is None:
                if not self.is_docpicture_directive(line):
                    new_lines.append(line)
                else:
                    text = '\n'.join(new_lines)
                    new_lines = []
                    self.body.append(svg.XmlElement("pre", text=text))
                    docpicture_lines.append(line)
            else:
                if self.is_docpicture_code(line):
                    docpicture_lines.append(line)
                else:
                    pre = svg.XmlElement("pre", text="\n".join(docpicture_lines))
                    pre.attributes["class"] = "docpicture"
                    self.body.append(pre)
                    flag, drawing = self.process_docpicture_code(docpicture_lines)

                    self.body.append(
                        )












def append_parser_result(new_lines, current_parser, lines_of_code):
    '''calls the appropriate parser to process the code and appends
    the result to the document being processed.'''
    result, errors = parse_code(current_parser,
            "\n".join(lines_of_code))
    if errors is not None:
        # We expect the parser to return a list of problem lines
        new_lines.append("<pre class='warning'>SYNTAX ERROR(S)")
        for err in errors:
            new_lines.append(err)
        new_lines.append("</pre>")
    new_lines.append(result)
    return

def test_circle(dummy_code):
    '''fake parser that returns the svg code to insert a circle
       inside a document'''
    return """
    <svg:svg width="300px" height="200px">
      <svg:circle cx="150px" cy="100px" r="50px" fill="#ff0000"
                             stroke="#000000" stroke-width="5px"/>
    </svg:svg>""", None

def null_defs():
    '''fake function to simulate returning defs'''
    return "<pre>Fake defs inserted before first picture is drawn.</pre>"

if __name__ == "__main__":
    src.parsers_loader.load_parsers()
    parsers = src.parsers_loader.PARSERS
    for parser in parsers:
        parsers_defs[parser] = parsers[parser].svg_defs()
    for parser in parsers_defs:
        print parsers_defs[parser]