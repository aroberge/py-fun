# parser for turtle docpicture directive

import re
from parsers._parser import _parser

_patterns = {
    # matching something like: turtle(42), and retain the value of the argument
    'turtle': re.compile("""
                turtle
                \s*\(\s*   # open paren (, possibly surrounded by spaces
                (\d+? | -\d+?)     # positive or negative integer as a group
                \s*\)      # close paren )
                $"""       # end of the (stripped) line
                , re.VERBOSE),
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
                \s*\)      # close paren )
                \.right\(\s*  # .left(
                (\d+? | -\d+?)     # positive or negative integer as a group
                \s*\)      # close paren )
                \s*->\s*   # ->
                turtle
                \s*\(\s*   # open paren (, possibly surrounded by spaces
                (\d+? | -\d+?)     # positive or negative integer as a group
                \s*\)      # close paren )
                $"""       # end of the (stripped) line
                , re.VERBOSE),
    # matching something like: turtle(42).forward(40) -> turtle(42)
    # and retains only the value of the argument to forward
    'forward': re.compile("""
                turtle
                \s*\(\s*   # open paren (, possibly surrounded by spaces
                -?\d+     # positive or negative integer NOT as a group
                \s*\)      # close paren )
                \.forward\(\s*  # .left(
                (\d+?)     # only positive integer as a group
                \s*\)      # close paren )
                \s*->\s*   # ->
                turtle
                \s*\(\s*   # open paren (, possibly surrounded by spaces
                -?\d+     # positive or negative integer NOT as a group
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
        <svg:filter id="turtle_filter" x="-30%" y="-30%" width="170%" height="170%">
          <svg:feGaussianBlur in="SourceAlpha" stdDeviation="8" result="turtle_filter"/>
          <svg:feOffset in="turtle_filter" dx="3" dy="3" result="offset_turtle_filter"/>
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
      <svg:circle cx="36px" cy="4px" r="2px" fill="darkgreen"/>
      <svg:circle cx="36px" cy="-4px" r="2px" fill="darkgreen"/>
      <!-- body -->
      <svg:ellipse cx="0px" cy="0px" rx="30px" ry="25px" fill="darkgreen"/>
    </svg:g>

    <svg:g id="black_plus">
        <svg:line x1="-6" x2="6" y1="0" y2="0" style="stroke:black; stroke-width:2"/>
        <svg:line x1="0" x2="0" y1="-6" y2="6" style="stroke:black; stroke-width:2"/>
    </svg:g>
    <svg:g id="start_to_start">
     <svg:use xlink:href="#black_plus" transform="translate(40, 0)"/>
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

