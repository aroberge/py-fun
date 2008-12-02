'''utilities.py

   a collection of functions used in other modules.

'''
import re
from xml.etree.ElementTree import Element, SubElement

import copy

def parse_vlam(vlam):
    parts = vlam.split()
    ret = {}
    for part in parts:
        pp = part.split('=', 1)
        if len(pp) >= 2:
            ret[pp[0]] = pp[1]
        else:
            ret[pp[0]] = ""
    return ret

def trim_empty_lines_from_end(text):
    '''remove blank lines at beginning and end of code sample'''
    # this is needed to prevent indentation error if a blank line
    # with spaces at different levels is inserted at the end or beginning
    # of some code to be executed.
    # This function is used in interpreter.py and colourize.py.
    return text.strip(' \r\n')

def changeHTMLspecialCharacters(text):
    '''replace <>& by their escaped valued so they are displayed properly
       in browser.'''
    # this function is used in colourize.py and cometIO.py
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def unChangeHTMLspecialCharacters(text):
    '''reverse of changeHTMLspecialCharacters'''
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    return text

def escape_for_javascript(text):
    '''as the name indicates, escape some characters so that they can be
       safely included in javascript'''
    text = text.replace("\\", "\\\\")
    text = text.replace("'", r"\'")
    text = text.replace('"', r'\"')
    text = text.replace("\n", r"\n")
    text = text.replace("\r", r"\r")
    return text

def insert_markup(elem, uid, vlam, markup, interactive_type):
    '''clears an element and inserts the new markup inside it'''
    elem.clear()
    elem.tag = "div"
    elem.attrib["id"] = "div_"+uid
    elem.attrib['class'] = interactive_type # 'editor', 'doctest', 'interpreter'
    if not "no_pre" in vlam:
        try:
            new_div = Element("div")
            new_div.append(markup)
            new_div.attrib['class'] = 'sample_python_code'
            elem.insert(0, new_div)
        except AssertionError:  # this should never happen
            elem.insert(0, Element("br"))
            bold = Element("b")
            span = Element("span")
            span.text = "AssertionError from ElementTree"
            bold.append(span)
            elem.insert(1, bold)

def wrap_in_div(elem, uid, vlam, element_type, show_vlam):
    '''wraps a styled code inside a div'''
    elem_copy = copy.deepcopy(elem)
    elem.clear()
    elem.text = ''
    elem.tag = "div"
    elem.attrib["id"] = "div_"+uid
    username = names[uid.split("_")[0]]
    # element_type = 'editor', 'doctest', etc.
    elem.attrib['class'] = element_type + " " + config[username]['style']
    if not "no_pre" in vlam:
        try:
            elem.append(elem_copy)
        except AssertionError:  # this should never happen
            elem.insert(0, Element("br"))
            bold = Element("b")
            span = Element("span")
            span.text = "AssertionError from ElementTree"
            bold.append(span)
            elem.insert(1, bold)
            return
    if show_vlam is not None:
        elem.insert(0, show_vlam)

def extract_code(elem):
    """extract all the text (Python code) from a marked up
    code sample encoded as an ElementTree structure, but converting
    <br/> into "\n" and removing "\r" which are not
    expected in Python code; inspired by F.Lundh's gettext()

    It also remove blank lines at beginning and end of code sample.
    """
    # The removal of blank lins is needed to prevent indentation error
    # if a blank line with spaces at different levels is inserted at the end
    # or beginning of some code to be executed.
    text = elem.text or ""
    for node in elem:
        text += extract_code(node)
        if node.tag == "br":
            text += "\n"
        if node.tail:
            text += node.tail
    text = text.replace("\r", "")
    return text

def is_interpreter_session(py_code):
    '''determine if the python code corresponds to a simulated
       interpreter session'''
    lines = py_code.split('\n')
    for line in lines:
        if line.strip():  # look for first non-blank line
            if line.startswith(">>>"):
                return True
            else:
                return False

def extract_code_from_interpreter(python_code):
    """ Strips fake interpreter prompts from html code meant to
        simulate a Python session, and remove lines without prompts, which
        are supposed to represent Python output.

        Assumes any '\r' characters have been removed from the Python code.
    """
    if not python_code:
        return
    lines = python_code.split('\n')
    new_lines = [] # will contain the extracted python code

    for line in lines:
        if line.startswith(">>> "):
            new_lines.append(line[4:].rstrip())
        elif line.rstrip() == ">>>": # tutorial writer may forget the
                                     # extra space for an empty line
            new_lines.append(' ')
        elif line.startswith("... "):
            new_lines.append(line[4:].rstrip())
        elif line.rstrip() == "...": # tutorial writer may forget the extra
            new_lines.append('')     # space for an empty line
        else: # output result
            pass
    python_code = '\n'.join(new_lines)
    return python_code
