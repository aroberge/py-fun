_parser.py tests
========================


    >>> from parsers import _parser
    >>> p = _parser.BaseParser()


Testing individual statements
-----------------------------

Testing statements like "turtle(42)"

    >>> p.parse_single_line("good")
    ('good', ())
    >>> p.parse_single_line("This is really good!")
    ('good', ())
    >>> p.parse_single_line("This is bad!")
    (None, 'This is bad!')


Now we move on to testing a series of statements. These are expected to
be received as a list of lines.

We first start with some failing examples.

    >>> test = ['good', 'really good', 'bad']
    >>> p.parse_lines_of_code(test)
    (['bad'], '')
    >>> error, drawing = p.parse_lines_of_code(test[:-1])
    >>> print error
    None
    >>> print drawing
    <pre>Drawing: ('good', ())
    Drawing: ('good', ())</pre>




