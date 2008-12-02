"""
perform vlam substitution

Adapted from file of the same name in Crunchy; the adaptation consists
mostly of major removal of elements.
"""

from StringIO import StringIO
from xml.etree import ElementTree as et

DTD = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '\
'"http://www.w3.org/TR/xhtml1/DTD/strict.dtd">\n'

class CrunchyPage(object):
    '''class used to store an html page processed by Crunchy with added
       interactive elements.
    '''
    # We define some class variables that will be shared amongst all instances.
    handlers3 = {} # tag -> attribute -> keyword -> handler function

    def __init__(self, file_content):
        """
        read a page, processes it and outputs a completely transformed one,
        ready for display in browser.
        """
        self.included = set([])
        self.count = 0
        # Create the proper tree structure from the html file
        self.tree = et.fromstring(file_content)

        self.head = self.tree.find("head")
        self.body = self.tree.find("body")
        # Crunchy's main work: processing vlam instructions.
        self.process_handlers3()
        # adding the javascript for communication between the browser and the server
        self.insert_js_file("/javascript/jquery.js")
        return

    def uidgen(self):
        """an suid (session unique ID) generator
        """
        self.count += 1
        return str(self.count)

    def add_include(self, include_str):
        '''keeps track of information included on a page'''
        self.included.add(include_str)

    def includes(self, include_str):
        '''returns information about string included on a page'''
        return include_str in self.included

    def add_css_code(self, code):
        '''inserts styling code in <head>'''
        css = et.Element("style", type="text/css")
        css.text = code
        self.head.insert(0, css)
        return

    def insert_css_file(self, path):
        '''inserts a link to the standard Crunchy style file'''
        css = et.Element("link", type= "text/css", rel="stylesheet",
                         href=path)
        self.head.append(css)
        return

    def add_js_code(self, code):
        ''' includes some javascript code in the <head>.
            This is the preferred method.'''
        js = et.Element("script", type="text/javascript")
        js.text = code
        self.head.append(js)
        return

    def insert_js_file(self, filename):
        '''Inserts a javascript file link in the <head>.
           This should only be used for really big scripts
           (like editarea); the preferred method is to add the
           javascript code directly'''
        js = et.Element("script", src=filename, type="text/javascript")
        js.text = " "  # prevents premature closing of <script> tag, misinterpreted by Firefox
        self.head.insert(0, js)
        return

    def extract_keyword(self, elem, attr):
        '''extract a "keyword" from a vlam string.

        A "keyword" is the first complete word in a vlam string; for
        example: vlam="keyword some other options"

        attr is assumed to be a valid key for elem[].
        '''
        try:
            keyword = [x for x in elem.attrib[attr].split(" ") if x != ''][0]
        except IndexError:
            keyword = None
        return keyword

    def process_handlers3(self):
        '''
        For all registered "tags" of "type 3", this method
        processes:  (tag, attribute, keyword) -> handler function
        '''
        for tag in self.handlers3:
            for elem in self.tree.getiterator(tag):
                # elem.attrib  size may change during the loop
                attributes = dict(elem.attrib)
                for attr in attributes:
                    if attr in self.handlers3[tag]:
                        keyword = self.extract_keyword(elem, attr)
                        if keyword in self.handlers3[tag][attr]:
                            self.handlers3[tag][attr][keyword]( self,
                                            elem, self.uidgen())
                            break

    def read(self):
        '''create fake file from a tree, adding DTD information
           and return its value as a string'''
        fake_file = StringIO()
        fake_file.write(DTD + '\n')
        fake_file.write(et.tostring(self.tree))
        return fake_file.getvalue()
