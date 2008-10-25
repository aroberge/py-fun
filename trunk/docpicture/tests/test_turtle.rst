t.py parser tests
========================


    >>> from parsers import turtle
    >>> t = turtle.Turtle()


Testing individual statements
-----------------------------

Testing statements like "turtle(42).left(42) -> turtle(84)".  Note that no
verification is done to ensure that angles add up properly.

    >>> t.parse_single_line("turtle(10).left(40) -> turtle(50)")
    ('left', ('10', '40', '50'))
    >>> t.parse_single_line("turtle(40).left(-10) -> turtle(30)")
    ('left', ('40', '-10', '30'))
    >>> t.parse_single_line("turtle( -40).left( -10 ) -> turtle( -50 )")
    ('left', ('-40', '-10', '-50'))

Testing statements like "turtle(42).right(42) -> turtle(0)". Note that no
verification is done to ensure that angles add up properly.

    >>> t.parse_single_line("turtle(10).right(40) -> turtle(-30)")
    ('right', ('10', '40', '-30'))
    >>> t.parse_single_line("turtle(40).right(-10) -> turtle(50)")
    ('right', ('40', '-10', '50'))
    >>> t.parse_single_line("turtle( -40).right( -41 ) -> turtle( 1 )")
    ('right', ('-40', '-41', '1'))

Testing statements like "turtle(42).forward(100) -> turtle(42)". Note that no
verification is done to ensure that angles add up properly, but we do
require positive numbers for the argument to forward()

    >>> t.parse_single_line("turtle(10).forward(40) -> turtle(10)")
    ('forward', ('10', '40', '10'))
    >>> t.parse_single_line("turtle( -40 ).forward( 433 ) -> turtle( -40 )")
    ('forward', ('-40', '433', '-40'))


Testing statements "turtle.up()" and "turtle.down()"

    >>> t.parse_single_line("turtle.up()")
    ('pen', ('up',))
    >>> t.parse_single_line("turtle.down()")
    ('pen', ('down',))
    >>> t.parse_single_line("turtle.up ()")
    (None, 'turtle.up ()')
    >>> t.parse_single_line("turtle.d()")
    (None, 'turtle.d()')

Testing statements like "turtle.color('red')"

    >>> t.parse_single_line("turtle.color('red')")
    ('color', ('red',))
    >>> t.parse_single_line('turtle.color(  "yellow"  )')
    ('color', ('yellow',))
    >>> t.parse_single_line('turtle.color(red)')
    (None, 'turtle.color(red)')


Now we move on to testing a series of statements. These are expected to
be received as a list of lines.

We first start with some failing examples.

    >>> test = ['turtle(1', 'turtle(10)', 'turtle.down()']
    >>> t.parse_lines_of_code(test)
    (['turtle(1', 'turtle(10)'], '')
    >>> t.parse_lines_of_code(test[1:])
    (['turtle(10)'], '')


    >>> test=['turtle(0).left(20) -> turtle(20)']
    >>> print t.parse_lines_of_code(test)[1]
      <svg:svg width="600" height="120">
        <svg:rect width="600" style="stroke:blue; stroke-width:1; fill:white" height="120"/>
        <svg:g filter="url(#turtle_filter)" transform="translate(60, 60)">
        <svg:use y="0" x="0" xlink:href="#turtle" transform="rotate(-0.0 0 0)"/>
    </svg:g>
        <svg:g filter="url(#turtle_filter)" transform="translate(300, 60)">
        <svg:use y="0" x="0" xlink:href="#turtle" transform="rotate(-20.0 0 0)"/>
    </svg:g>
        <svg:use xlink:href="#start_to_start" transform="translate(0, 60)"/>
        <svg:text y="65" x="150">
      left(20)
    </svg:text>
    </svg:svg>
    <BLANKLINE>
