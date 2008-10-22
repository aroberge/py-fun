'''

docpicture

Need to explain what it does here
'''


import re


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
def identify_docpicture_directive(line):
    """ Identifies if a line corresponds to a docpicture directives.

        If it is a docpicture directive, it returns the indentation (number of
        spaces at the beginning of the line) and the name of the processor;
        otherwise it returns None.
    """
    result = docpicture_directive_pattern.search(line.rstrip())
    if result is None:
        return None
    else:
        return line.index("..docpicture"), result.groups()[0]

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
        return "<p class='warning'>Unknown parser %s.</p>" % parser, None

def parse_document(text):
    '''parses an entire document, received as a string, and outputs
    an html document with svg code inserted by the appropriate parser.
    The original text is inserted into some pre-formatted sections,
    so as to retain the original look - including any existing ascii diagrams.
    '''
    lines = text.split("\n")
    new_lines = [BEGIN_DOCUMENT, "<p>\n"]
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
                new_lines.append("<p>\n"+line)
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
                new_lines.append("</p>\n<pre class='docpicture'>")
            new_lines.append(line)
    # We have to guard against the situation where we ended with a docpicture
    if lines_of_code is not None:
        new_lines.append("</pre>")
        append_parser_result(new_lines, current_parser, lines_of_code)
        new_lines.append(END_DOCUMENT)
    else:
        new_lines.append("</p>\n"+END_DOCUMENT)
    return "\n".join(new_lines)

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
