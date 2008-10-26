'''
This module contains all the classes required to easily create an xml
document containing svg diagrams.

'''

class XmlElement(object):
    '''Prototype from which all the xml elements are derived.

       By design, this enables all elements to automatically give a
       text representation of themselves.'''

    def __init__(self, tag, **attributes):
        '''A basic definition that will be replaced by the specific
           one required by any element.'''
        self.tag = tag
        self.prefix = ""
        self.sub_elements = []
        if attributes is not None:
            self.attributes = attributes
        else:
            self.attributes = {}

    def __repr__(self):
        '''This normal python method used to give a string representation
        for an object is used to automatically create the appropriate
        syntax representing an xml object.'''
        attrib = ["  <%s%s"%(self.prefix, self.tag)] # open tag
        for att in self.attributes:
            if att != 'text':
                attrib.append(' %s="%s"' % (att, self.attributes[att]))
        if 'text' in self.attributes:
            attrib.append(">%s</%s%s>\n" % (self.attributes['text'],
                                                    self.prefix, self.tag))
        elif self.sub_elements:
            attrib.append(">\n")
            for elem in self.sub_elements:
                attrib.append("  %s" % elem)
            attrib.append("</%s%s>\n" % (self.prefix, self.tag))
        else:
            attrib.append("/>\n")
        return ''.join(attrib)

    def append(self, other):
        '''append other to self to create list of lists of elements'''''
        self.sub_elements.append(other)


class XmlDocument(XmlElement):
    def __init__(self):
        self._begin = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:svg="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink">\n"""
        self._end = "</html>"
        self.head = XmlElement("head")
        self.body = XmlElement("body")

    def append(self):
        '''Direclty appending is not allowed'''
        assert False, "Append to either head or body."

    def __repr__(self):
        '''Gives an appropriate representation of an xml document.'''
        return self._begin + str(self.head) + str(self.body) + self._end


class SvgElement(XmlElement):
    '''Prototype from which all the svg elements are derived.

       By design, this enables all elements to automatically give an
       appropriate text representation of themselves.'''
    def __init__(self, tag, **attributes):
        XmlElement.__init__(self, tag, **attributes)
        self.prefix = "svg:"

class SvgDefs(SvgElement):
    '''Short-cut to create svg defs.  A user creates an instance of this
    object and simply appends other svg Elements'''
    def __init__(self):
        self.defs = SvgElement("defs")
        self.root = SvgElement("svg", width=0, height=0)
        self.root.append(self.defs)

    def append(self, other):
        '''appends other to defs sub-element, instead of root element'''
        self.defs.append(other)

    def __repr__(self):
        '''gives a string representation of an object, appropriate for
           insertion in an html document'''
        return str(self.root)

class Comment(object):
    '''Comment that can be inserted in code xml documents'''
    def __init__(self, text):
        self.text = text
    def __repr__(self):
        return "<!-- " + self.text + " -->\n"

if __name__ == "__main__":
    test_doc = XmlDocument()
    test_doc.head.append(XmlElement("title", text="This is the title."))

    # A good practice is to define svg objects, and insert them
    # using the definition; this is overkill for this example, but it
    # provides a test of the class.
    test_def = SvgDefs()
    test_def.append(SvgElement("circle", cx=0, cy=0, r=20, fill="red",
                            id="red_circle"))

    test_doc.body.append(XmlElement("p", text="This is the body."))
    test_doc.body.append(test_def)

    # we now create an svg object, that will make use of the definition above.
    svg_window = SvgElement("svg", width="200", height="200")
    use_circle = SvgElement("use", transform="translate(100, 100)")
    # xlink:href can't be used as an attribute name passed to __init__
    # this is why we use this two-step process.
    use_circle.attributes["xlink:href"] = "#red_circle"

    svg_window.append(use_circle)
    test_doc.body.append(svg_window)
    test_doc.body.append(Comment("This is a comment.")) # just as a test.
    print test_doc
