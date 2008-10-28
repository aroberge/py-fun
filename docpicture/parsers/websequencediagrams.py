'''  Parser for the web_sequence diagrams
http://www.websequencediagrams.com
directive
'''

import re
from _parser import BaseParser
import src.svg as svg

_patterns = {
    # anything is declared to be good; we let the website worry about it.
    'any': re.compile("^(.*?)$")
}

def register_docpicture_parser(register_parser):
    register_parser(WebSequence)

class WebSequence(BaseParser):
    '''a parser creating web sequence diagrams'''
    def __init__(self):
        self.patterns = _patterns
        self.directive_name = 'websequence'

    def get_svg_defs(self):
        '''No svg diagrams produced by this parser.'''
        return svg.Comment("ignore me")

    def draw(self, lines):
        '''Insert appropriate reference so that graphics can be
        loaded from website'''
        div = svg.XmlElement("div", wsd_style="modern-blue")
        div.attributes['class'] = "wsd"
        relevant_text = []
        for line in lines:
            for items in line[1::2]:
                relevant_text.append(items[0])
        text = "\n".join(relevant_text)
        div.append(svg.XmlElement("pre", text=text))
        main_div = svg.XmlElement("div")
        main_div.append(div)
        main_div.append(svg.XmlElement("script",
                            type="text/javascript",
                            src="http://www.websequencediagrams.com/service.js"))
        return main_div
