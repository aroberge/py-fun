'''styles the code using Pygments'''
import re
from xml.etree.ElementTree import fromstring

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from pygments.lexers._mapping import LEXERS

from src.utilities import extract_code

_pygment_lexer_names = {}
_pygment_language_names = []
for name in LEXERS:
    aliases = LEXERS[name][2]
    _pygment_lexer_names[name] = aliases[0]
    for alias in aliases:
        _pygment_language_names.append(alias)

lexers = {}

def pygments_style(page, elem, dummy_uid='42'):
    cssclass = 'tango'
    if 'class' in elem.attrib:
        if 'doctest-block' in elem.attrib['class']:
            elem.attrib['title'] = 'pycon'
    language = elem.attrib['title'].split()[0]
    if language in ['py_code', 'python_code']:
        language = "python"
    text = extract_code(elem)
    styled_code = _style(text, language, cssclass).encode("utf-8")
    vlam = elem.attrib['title']
    if 'linenumber' in vlam:
        styled_code = add_linenumber(styled_code, vlam)
    markup = fromstring(styled_code)
    elem[:] = markup[:]
    elem.text = markup.text
    elem.attrib['class'] = cssclass
    if not page.includes("pygment_cssclass"):
        # replacing class name for security reasons.
        page.add_css_code(HtmlFormatter(style=cssclass).get_style_defs("."+cssclass))
        page.add_include("pygment_cssclass")
    return text


class PreHtmlFormatter(HtmlFormatter):
    '''unlike HtmlFormatter, does not embed the styled code inside both
       a <div> and a <pre>; rather embeds it inside a <pre> only.'''

    def wrap(self, source, dummy):
        return self._wrap_code(source)

    def _wrap_code(self, source):
        yield 0, '<pre>\n'
        for i, t in source:
            yield i, t
        yield 0, '</pre>'


def _style(raw_code, language, cssclass):
    """Returns a string of formatted and styled HTML, where
    raw_code is a string, language is a string that Pygments has a lexer for,
    and cssclass is a class style available for Pygments."""

    requested_language = language
    try:
        lexer = lexers[language]
    except:
        lexers[language] = get_lexer_by_name(language, stripall=True)
        lexer = lexers[requested_language]

    formatter = PreHtmlFormatter()
    formatter.cssclass = cssclass
    formatter.style = get_style_by_name(cssclass)

    # the removal of "\n" below prevents an extra space to be introduced
    # with the background color of the selected cssclass
    return highlight(raw_code, lexer, formatter).replace("\n</pre>", "</pre>")

def add_linenumber(styled_code, vlam):
    '''adds the line number information'''
    lines = styled_code.split('\n')
    # is the class surrounded by quotes or double quotes?
    prompt1 = '<span class="gp"'
    prompt2 = "<span class='gp'"
    if lines[1].startswith(prompt1):
        prompt_present = True
        prompt = prompt1
    elif lines[1].startswith(prompt2):
        prompt_present = True
        prompt = prompt2
    else:
        prompt_present = False
    lineno = get_linenumber_offset(vlam)
    # first and last lines are the embedding <pre>...</pre>
    open_span = "<span class = 'linenumber c'>"
    for index, line in enumerate(lines[1:-1]):
        if prompt_present:
            if lines[index+1].startswith(prompt):
                lines[index+1] = open_span + "%3d </span>" % (lineno) + line
                lineno += 1
            else:
                lines[index+1] = open_span + "    </span>" + line
        else:
            lines[index+1] = open_span + "%3d </span>" % (lineno) + line
            lineno += 1
    return '\n'.join(lines)

def get_linenumber_offset(vlam):
    """ Determine the desired number for the 1st line of Python code.
        The vlam code is expected to be of the form
        [linenumber [=n]]    (where n is an integer).
    """
    try:
        res = re.search(r'linenumber\s*=\s*([0-9]*)', vlam)
        offset = int(res.groups()[0])
    except:
        offset = 1
    return offset