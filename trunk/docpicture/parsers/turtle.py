# parser for turtle docpicture directive

import math
import re
from parsers._parser import _parser
from src import svg

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

_svg_defs = """
<svg:svg width="0" height="0">
    <svg:defs>
    <!-- filter idea adapted from "SVG for Web Developers" by Pearlman and House-->
        <svg:filter id="turtle_filter" x="-35%" y="-35%" width="170%" height="170%">
          <svg:feGaussianBlur in="SourceAlpha" stdDeviation="8" result="turtle_filter"/>
          <svg:feOffset in="turtle_filter" dx="-3" dy="-3" result="offset_turtle_filter"/>
          <svg:feSpecularLighting in="turtle_filter" surfaceScale="4"
                specularConstant=".95" specularExponent="17"
                lighting-color="#cccc66" result="light_turtle">
                <svg:feDistantLight elevation="40" azimuth="60"/>
          </svg:feSpecularLighting>
          <svg:feComposite in="light_turtle" in2="SourceAlpha" operator="in"
               result="light_turtle2"/>
          <svg:feComposite in="SourceGraphic" in2="light_turtle2"
                operator="arithmetic" k1="0" k2=".9" k3="1" k4="0"
                result="turtle_lit"/>
          <svg:feMerge>
            <svg:feMergeNode in="offset_turtle_filter"/>
            <svg:feMergeNode in="turtle_lit"/>
          </svg:feMerge>
        </svg:filter>

    <svg:g id="turtle">
       <!-- legs -->
      <svg:circle cx="23px" cy="16px" r="8px" fill="tan"/>
      <svg:circle cx="23px" cy="-15px" r="8px" fill="tan"/>
      <svg:circle cx="-23px" cy="16px" r="8px" fill="tan"/>
      <svg:circle cx="-23px" cy="-15px" r="8px" fill="tan"/>
      <!-- head and eyes-->
      <svg:circle cx="32px" cy="0px" r="8px" fill="tan"/>
      <svg:circle cx="36px" cy="4px" r="2px" fill="black"/>
      <svg:circle cx="36px" cy="-4px" r="2px" fill="black"/>
      <!-- body -->
      <svg:ellipse cx="0px" cy="0px" rx="30px" ry="25px" fill="darkgreen"/>
    </svg:g>

    <svg:g id="black_plus">
        <svg:line x1="-6" x2="6" y1="0" y2="0" style="stroke:black; stroke-width:2"/>
        <svg:line x1="0" x2="0" y1="-6" y2="6" style="stroke:black; stroke-width:2"/>
    </svg:g>
    <svg:g id="start_to_start">
     <svg:use xlink:href="#black_plus" transform="translate(60, 0)"/>
     <svg:use xlink:href="#black_plus" transform="translate(300, 0)"/>
     </svg:g>
    </svg:defs>
</svg:svg>"""


default_drawing = {
    'angle1': 0,
    'angle2': 0,
    'action': 'left',
    'color': 'black',
    'pen': 'down',
    'distance': 200,
}

class turtle(_parser):
    def __init__(self):
        self.svg_defs = _svg_defs  # reference to global definition
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
        self.compute_drawing_parameters(lines)
        return self.create_svg_code()

    def compute_drawing_parameters(self, lines):
        self.set_defaults()  # reset values
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

    def create_svg_code(self):
        window = svg.Element("svg", width=self.width, height=self.height)
        window.append(svg.Element("rect", width=self.width, height=self.height,
                                style="stroke:blue; stroke-width:1; fill:white"))
        if self.pen_down:
            window.append(svg.Element("line", x1=self.x1+self.gap_between_turtles,
                                      y1=self.y1, x2=self.x2, y2=self.y2,
                                      style="stroke:%s; stroke-width:4;"%self.color))
        # first turtle
        t1 = svg.Element("g", transform="translate(%d, %d)"%(self.x1, self.y1),
                         filter="url(#turtle_filter)")
        _t1 = svg.Element("use", x=0, y=0, transform="rotate(%s 0 0)"%(-float(self.angle1)))
        _t1.attributes["xlink:href"] = "#turtle"
        t1.append(_t1)
        window.append(t1)
        # second turtle
        t2 = svg.Element("g", transform="translate(%d, %d)"%(self.x2, self.y2),
                         filter="url(#turtle_filter)")
        _t2 = svg.Element("use", x=0, y=0, transform="rotate(%s 0 0)"%(-float(self.angle2)))
        _t2.attributes["xlink:href"] = "#turtle"
        t2.append(_t2)
        window.append(t2)
        # plus signs indicating center of initial turtle position
        plus = svg.Element("use", transform="translate(0, %d)"%self.y1)
        plus.attributes["xlink:href"] = "#start_to_start"
        window.append(plus)
        # text for command
        window.append(svg.Element("text", x=self.text_x, y=self.text_y,
                                  text="%s(%s)"%(self.command, self.arg)))
        return str(window)
