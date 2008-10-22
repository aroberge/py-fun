docpicture.py tests
====================


    >>> import docpicture

First, we make sure that there has not been any accidental changes made
to the Doctype and other information.
    >>> print docpicture.BEGIN_DOCUMENT
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE html
        PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:svg="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink">
      <head>
        <style>
            p{width:800px;}
            pre{font-size: 12pt;}
            .docpicture{color: blue;}
            .warning{color: red;}
        </style>
      </head>
    <body>

Next, we reassign these values so that we will be able to test
whole documents processing while reducing the output.

    >>> docpicture.BEGIN_DOCUMENT = "==Begin=="
    >>> docpicture.END_DOCUMENT = "==End=="

Testing identify_docpicture_directive(). First a simple case.

    >>> doc_line = "..docpicture:: some_name"
    >>> print docpicture.identify_docpicture_directive(doc_line)
    (0, 'some_name')

Same example but with extra space at the beginning and no space between the two
colons and the name.
    >>> doc_line = "    ..docpicture::some_name"
    >>> print docpicture.identify_docpicture_directive(doc_line)
    (4, 'some_name')

Some spaces in the processor name
    >>> doc_line = " ..docpicture:: some name"
    >>> print docpicture.identify_docpicture_directive(doc_line)
    (1, 'some name')

A failing example (only one dot at the beginning.
    >>> doc_line = ".docpicture:: some_name"
    >>> print docpicture.identify_docpicture_directive(doc_line)
    None

Next, we need to identify docpicture code.  docpicture code is,
by definition, indented at least one more space than the docpicture directive
declaration.  To make the code more readable, empty lines (with only blank
spaces) are considered to be part of the docpicture code.  They are also
preserved as a docpicture code parser may be designed to use this information.

    >>> test_code = "    Line with 4 spaces at the beginning."
    >>> print docpicture.is_code(test_code, 4)
    False
    >>> print docpicture.is_code(test_code, 3)
    True
    >>> print docpicture.is_code(test_code, 5)
    False
    >>> print docpicture.is_code(test_code, 2)
    True
    >>> print docpicture.is_code("   ", 18)
    True

Next, we need to be able to call the appropriate parser, and give a useful
error message.  As we don't have any parsers in this module, we will
simply test the error message.

    >>> print docpicture.parse_code('parser_name', 'test_code')
    ("<p class='warning'>Unknown parser parser_name.</p>", None)

We are now ready to parse an entire document, extracting
the directive names, code and processing it accordingly.

    >>> test_document = """\
    ... This is a test.
    ... It has many lines.
    ... ..docpicture:: first
    ...    Some code
    ...   More code
    ... 
    ...     Even more code
    ...
    ... Back to normal text.
    ... Some more text.
    ...     ..docpicture:: second (indented line)
    ...        part of the code
    ...     Not part of the code (same indentation as ..docpicture declaration)
    ... End of text."""
    >>> print docpicture.parse_document(test_document)
    ==Begin==
    <p>
    <BLANKLINE>
    This is a test.
    It has many lines.
    </p>
    <pre class='docpicture'>
    ..docpicture:: first
       Some code
      More code
    <BLANKLINE>
        Even more code
    <BLANKLINE>
    </pre>
    <p class='warning'>Unknown parser first.</p>
    <p>
    Back to normal text.
    Some more text.
    </p>
    <pre class='docpicture'>
        ..docpicture:: second (indented line)
           part of the code
    </pre>
    <p class='warning'>Unknown parser second (indented line).</p>
    <p>
        Not part of the code (same indentation as ..docpicture declaration)
    End of text.
    </p>
    ==End==

