t.py parser tests
========================


    >>> from parsers import turtle
    >>> t = turtle.turtle()


Testing individual statements
-----------------------------

Testing statements like "turtle(42)"

    >>> t.parse_single_line("turtle(0)")
    ('turtle', ('0',))
    >>> t.parse_single_line(" turtle ( 23 ) ")
    ('turtle', ('23',))
    >>> t.parse_single_line("turtle()")
    (None, 'turtle()')
    >>> t.parse_single_line("turtle(-42)")
    ('turtle', ('-42',))

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
    ('forward', ('40',))
    >>> t.parse_single_line("turtle( -40 ).forward( 433 ) -> turtle( -40 )")
    ('forward', ('433',))


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

    >>> test = ['turtle(1', 'turtle(10)', 't']
    >>> t.parse_lines_of_code(test)
    (['turtle(1', 't'], '')
    >>> t.parse_lines_of_code(test[1:])
    (['t'], '')




