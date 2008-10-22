class Element(object):
    '''Prototype from which all the svg elements are derived.

       By design, this enables all elements to automatically give a
       text representation of themselves.'''

    def __init__(self, tag, **attributes):
        '''A basic definition that will be replaced by the specific
           one required by any element.'''
        self.open_tag = "<svg:%s" % tag
        self.tag = tag
        self.sub_elements = []
        if attributes is not None:
            self.attributes = attributes
        else:
            self.attributes = {}

    def __repr__(self):
        '''This normal python method used to give a string representation
        for an object is used to automatically create the appropriate
        syntax representing an svg object.'''
        attrib = [self.open_tag]
        for att in self.attributes:
            if att != 'text':
                attrib.append(' %s="%s"' % (att, self.attributes[att]))
        if 'text' in self.attributes:
            attrib.append(">\n  %s\n</svg:text>\n" % self.attributes['text'])
        elif self.sub_elements:
            attrib.append(">\n")
            for elem in self.sub_elements:
                attrib.append("  %s" % elem)
            attrib.append("</svg:%s>\n" % self.tag)
        else:
            attrib.append("/>\n")
        return ''.join(attrib)

    def append(self, other):
        self.sub_elements.append(other)