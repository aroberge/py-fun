'''  Parser for the turtle docpicture directive

'''

import math
import re
from _parser import BaseParser
from .src import svg

_patterns = {
    # matching something like: turtle(42).left(-40) -> turtle(2)
    # and retains the value of the 3 function arguments
    'left': re.compile("""
                turtle
                \s*\(\s*   # open paren (, possibly surrounded by spaces
                (\d+? | -\d+?)     # positive or negative integer as a group
                \s*\)      # close paren )
                \.left\(\s*  # .left(
                (\d+? | -\d+?)     # positive or negative integer as a group
                \s*\)      # close paren )
                \s*->\s*   # ->
                turtle
                \s*\(\s*   # open paren (, possibly surrounded by spaces
                (\d+? | -\d+?)     # positive or negative integer as a group
                \s*\)      # close paren )
                $"""       # end of the (stripped) line
                , re.VERBOSE),
    # matching something like: turtle(42).right(-40) -> turtle(82)
    # and retains the value of the 3 function arguments
    'right': re.compile("""
                turtle
                \s*\(\s*   # open paren (, possibly surrounded by spaces
                (\d+? | -\d+?)     # positive or negative integer as a group
                \s*\)
                \.right\(\s*
                (\d+? | -\d+?)     # positive or negative integer as a group
                \s*\)      # close paren )
                \s*->\s*   # ->
                turtle
                \s*\(\s*
                (\d+? | -\d+?)     # positive or negative integer as a group
                \s*\)      # close paren )
                $"""       # end of the (stripped) line
                , re.VERBOSE),
    # matching something like: turtle(42).forward(-40) -> turtle(82)
    # and retains the value of the 3 function arguments
    'forward': re.compile("""
                turtle
                \s*\(\s*   # open paren (, possibly surrounded by spaces
                (\d+? | -\d+?)     # positive or negative integer as a group
                \s*\)      # close paren )
                \.forward\(\s*  # .forward(
                (\d+? | -\d+?)     # positive or negative integer as a group
                \s*\)      # close paren )
                \s*->\s*   # ->
                turtle
                \s*\(\s*   # open paren (, possibly surrounded by spaces
                (\d+? | -\d+?)     # positive or negative integer as a group
                \s*\)      # close paren )
                $"""       # end of the (stripped) line
                , re.VERBOSE),
    # matching either "turtle.up()" or "turtle.down()"
    # retaining only "up" or "down"
    'pen': re.compile("""
                turtle\.
                (up? | down?)
                \(\)$""", re.VERBOSE),
    # matching something like: turtle.color("red"), and retain the value of the argument
    'color': re.compile(r"""
                turtle\.color
                \s*\(\s*   # open paren (, possibly surrounded by spaces
                ["']([a-zA-Z]+?)["'] # color...
                \s*\)      # close paren )
                $"""       # end of the (stripped) line
                , re.VERBOSE),
}


class Turtle(BaseParser):
    '''a parser creating "nice" turtle pictures'''
    def __init__(self):
        self.patterns = _patterns  # definitely needs to be overriden!
        self.width = 600
        self.max_height = 600
        self.min_height = 120
        self.gap_between_turtles = 240
        self.size = 60
        self.min_y = self.size   # minimum value of position for first turtle
        self.max_y = self.max_height - self.size
        self.x1 = 60
        self.text_x = 150  # position of text for command
        self.set_defaults()

    def svg_defs(self):
        '''returns an object representing all the svg defs'''
        defs = svg.SvgDefs()
        defs.append(self.turtle_defs())
        defs.append(self.filter_defs())
        defs.append(self.plus_signs_defs())
        return defs

    def set_defaults(self):
        '''set default values for coordinates'''
        self.y1 = 60
        self.height = 120
        self.color = 'black'
        self.pen_down = False
        self.command = None

    def draw(self, lines):
        '''fake function; normally would convert parsed lines of code
           into svg drawing statements'''
        self.compute_layout_parameters(lines)
        return self.create_svg_object()

    def compute_layout_parameters(self, lines):
        '''calculate numerical parameters (angle, position, etc.) to draw
        the turtles'''
        self.set_defaults()
        for line in lines:
            if line[0] in ['forward', 'left', 'right']:
                self.command, (self.angle1, self.arg, self.angle2) = line
            elif line[0] == 'color':
                self.color = line[1][0]
            elif line[0] == 'pen':
                self.pen_down = (line[1][0] == 'down')
            else:
                assert False, "Unknown command %s in locate_turtles." % line[0]

        assert self.command != None, 'Invalid set of lines passed to locate_turtles'
        if self.command == 'forward':
            dx = float(self.arg)*math.cos(math.radians(float(self.angle1)))
            dy = float(self.arg)*math.sin(math.radians(float(self.angle1)))
        else:
            dx = dy = 0
        dx = int(dx)
        dy = int(dy)
        # location of first turtle; self.x1 is fixed
        self.y1 += dy
        if not self.min_y <= self.y1 <= self.max_y:
            self.y1 = min(self.y1, self.max_y)
            self.y1 = max(self.y1, self.min_y)
        self.y1 = int(self.y1)

        # location of second turtle
        self.x2 = self.x1 + self.gap_between_turtles + dx
        self.y2 = self.y1 - dy

        # window size; self.width is fixed
        self.height = self.y1 + self.size
        if float(self.angle2) <=0:
            self.height = min(self.y2 + self.size, self.max_y)

        # vertical position of text
        self.text_y = self.y1 + 5
        return

    def create_svg_object(self):
        '''creates the svg object required to draw the turtles'''
        window = svg.SvgElement("svg", width=self.width, height=self.height)
        window.append(self.image_frame())
        if self.pen_down:
            window.append(self.line_trace())
        window.append(self.first_turtle())
        window.append(self.second_turtle())
        window.append(self.plus_signs())
        # text for command
        window.append(svg.SvgElement("text", x=self.text_x, y=self.text_y,
                                  text="%s(%s)"%(self.command, self.arg)))
        return window

    def image_frame(self):
        '''creates a frame for the image'''
        return svg.SvgElement("rect", width=self.width, height=self.height,
                                style="stroke:blue; stroke-width:1; fill:white")

    def line_trace(self):
        '''creates the code for the line traced by the turtle'''
        return svg.SvgElement("line", x1=self.x1+self.gap_between_turtles,
                                      y1=self.y1, x2=self.x2, y2=self.y2,
                                      style="stroke:%s; stroke-width:4;"%self.color)


    def first_turtle(self):
        '''creation of first turtle'''
        t1 = svg.SvgElement("g", transform="translate(%d, %d)"%(self.x1, self.y1),
                         filter="url(#turtle_filter)")
        _t1 = svg.SvgElement("use", x=0, y=0, transform="rotate(%s 0 0)"%(-float(self.angle1)))
        _t1.attributes["xlink:href"] = "#turtle"
        t1.append(_t1)
        return t1

    def second_turtle(self):
        '''creation of second turtle'''
        t2 = svg.SvgElement("g", transform="translate(%d, %d)"%(self.x2, self.y2),
                         filter="url(#turtle_filter)")
        _t2 = svg.SvgElement("use", x=0, y=0, transform="rotate(%s 0 0)"%(-float(self.angle2)))
        _t2.attributes["xlink:href"] = "#turtle"
        t2.append(_t2)
        return t2

    def plus_signs(self):
        '''create the two plus signs indicating the initial center location of
        the turtle'''
        plus = svg.SvgElement("use", transform="translate(0, %d)"%self.y1)
        plus.attributes["xlink:href"] = "#start_to_start"
        return plus

    def turtle_defs(self):
        '''creates the svg:defs content for the turtle'''
        t = svg.SvgElement("g", id="turtle")
        # legs
        t.append(svg.SvgElement("circle", cx=23, cy=16, r=8, fill="tan"))
        t.append(svg.SvgElement("circle", cx=23, cy=-15, r=8, fill="tan"))
        t.append(svg.SvgElement("circle", cx=-23, cy=16, r=8, fill="tan"))
        t.append(svg.SvgElement("circle", cx=-23, cy=-15, r=8, fill="tan"))
        # head and eyes
        t.append(svg.SvgElement("circle", cx=32, cy=0, r=8, fill="tan"))
        t.append(svg.SvgElement("circle", cx=36, cy=4, r=2, fill="black"))
        t.append(svg.SvgElement("circle", cx=36, cy=-4, r=2, fill="black"))
        # body
        t.append(svg.SvgElement("ellipse", cx=0, cy=0, rx=30, ry=25,
                                fill="darkgreen"))
        return t

    def filter_defs(self):
        '''create the svg:defs content for the filter used to transform
        a flat turtle image into something that looks more three-dimensional'''
        # filter idea adapted from "SVG for Web Developers" by Pearlman and House

        f = svg.SvgElement("filter", id="turtle_filter", x="-35%", y="-35%",
                           width="170%", height="170%")
        blur = svg.SvgElement("feGaussianBlur", stdDeviation=8,
                              result="turtle_filter")
        blur.attributes['in'] = "SourceAlpha"
        f.append(blur)
        offset = svg.SvgElement("feOffset", dx=-3, dy=-3,
                              result="offset_turtle_filter")
        offset.attributes['in'] = "turtle_filter"
        f.append(offset)
        specular = svg.SvgElement("feSpecularLighting", surfaceScale=4,
                                  specularConstant=.95, specularExponent=17,
                                  result="light_turtle")
        specular.attributes['in'] = "turtle_filter"
        specular.attributes['lighting-color'] = "#cccc66"
        specular.append(svg.SvgElement("feDistantLight", elevation=40,
                                       azimuth=60))
        f.append(specular)
        comp1 = svg.SvgElement("feComposite", in2="SourceAlpha", operator="in",
                               result="light_turtle2")
        comp1.attributes["in"] = "light_turtle"
        f.append(comp1)
        comp2 = svg.SvgElement("feComposite", in2="light_turtle2",
                               operator="arithmetic", k1=0, k2=.9, k3=1, k4=0,
                               result="turtle_lit")
        comp2.attributes["in"] = "SourceGraphic"
        f.append(comp2)
        merge = svg.SvgElement("feMerge")
        node1 = svg.SvgElement("feMergeNode")
        node1.attributes["in"] = "offset_turtle_filter"
        merge.append(node1)
        node2 = svg.SvgElement("feMergeNode")
        node2.attributes["in"] = "turtle_lit"
        merge.append(node2)
        f.append(merge)
        return f

    def plus_signs_defs(self):
        '''create the svg:defs for the two plus signs used to indicate
        the initial position of the turtle'''
        p = svg.SvgElement("g", id="start_to_start")
        _style = "stroke:black; stroke-width:2"
        p.append(svg.SvgElement("line", x1=54, x2=66, y1=0, y2=0, style=_style))
        p.append(svg.SvgElement("line", x1=60, x2=60, y1=-6, y2=6, style=_style))
        p.append(svg.SvgElement("line", x1=294, x2=306, y1=0, y2=0, style=_style))
        p.append(svg.SvgElement("line", x1=300, x2=300, y1=-6, y2=6, style=_style))
        return p

class ColorTurtle(Turtle):

    def svg_defs(self):
        '''returns an object representing all the svg defs'''
        defs = svg.SvgDefs()
        defs.append(self.turtle_defs())
        # same as Turtle but with no filter
        #defs.append(self.filter_defs())
        defs.append(self.plus_signs_defs())
        return defs

    def first_turtle(self):
        '''creation of first turtle '''
        # same as Turtle, except no filter
        t1 = svg.SvgElement("g", transform="translate(%d, %d)"%(self.x1, self.y1))
        _t1 = svg.SvgElement("use", x=0, y=0, transform="rotate(%s 0 0)"%(-float(self.angle1)))
        _t1.attributes["xlink:href"] = "#turtle"
        t1.append(_t1)
        return t1

    def second_turtle(self):
        '''creation of second turtle'''
        # same as Turtle, except no filter
        t2 = svg.SvgElement("g", transform="translate(%d, %d)"%(self.x2, self.y2))
        _t2 = svg.SvgElement("use", x=0, y=0, transform="rotate(%s 0 0)"%(-float(self.angle2)))
        _t2.attributes["xlink:href"] = "#turtle"
        t2.append(_t2)
        return t2


def test_me():
    import src.server as server
    import time
    import sys
    t = Turtle()
    t2 = ColorTurtle()

    test_doc = svg.XmlDocument()
    test_doc.head.append(svg.XmlElement("title", text="This is the title."))
    test_doc.body.append(t.svg_defs())
    lines = ['turtle.down()', 'turtle.color("red")',
             'turtle(20).forward(200) -> turtle(20)']
    test_doc.body.append(svg.XmlElement("pre", text='\n'.join(lines)))
    error, drawing_object = t.parse_lines_of_code(lines)
    if error is None:
        test_doc.body.append(drawing_object)

    error, drawing_object = t2.parse_lines_of_code(lines)
    if error is None:
        test_doc.body.append(drawing_object)

    server.Document(str(test_doc))
    threaded_server = server.ServerInThread()
    threaded_server.start()

    print "Server will be active for 10 seconds."
    for i in range(10, 0, -1):
        print i,
        sys.stdout.flush()
        time.sleep(1)

    server.stop_server(threaded_server.port)
    print "Done!"

if __name__ == "__main__":
    test_me()