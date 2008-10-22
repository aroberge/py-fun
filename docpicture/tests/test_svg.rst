Svg stuff
==========

Here we test the creation of various elements.

    >>> import src.svg as svg

    >>> elem = svg.Element("line")
    >>> print elem
    <svg:line/>
    <BLANKLINE>
    >>> elem = svg.Element("circle", cx=10, cy=30, r="10", color="red")
    >>> print elem
    <svg:circle color="red" cy="30" cx="10" r="10"/>
    <BLANKLINE>
    >>> elem = svg.Element("text", text="This is a test.")
    >>> print elem
    <svg:text>
      This is a test.
    </svg:text>
    <BLANKLINE>
    >>> elem = svg.Element("g")
    >>> elem2 = svg.Element("circle", cx=10, cy=30, r="10", color="red")
    >>> elem.append(elem2)
    >>> print elem
    <svg:g>
      <svg:circle color="red" cy="30" cx="10" r="10"/>
    </svg:g>
    <BLANKLINE>
    >>> elem3 = svg.Element("circle", cx=10, cy=40, r="10", color="yellow")
    >>> elem.append(elem3)
    >>> print elem
    <svg:g>
      <svg:circle color="red" cy="30" cx="10" r="10"/>
      <svg:circle color="yellow" cy="40" cx="10" r="10"/>
    </svg:g>
    <BLANKLINE>
    >>> elem1 = svg.Element("g")
    >>> elem1.append(elem)
    >>> print elem1
    <svg:g>
      <svg:g>
        <svg:circle color="red" cy="30" cx="10" r="10"/>
        <svg:circle color="yellow" cy="40" cx="10" r="10"/>
      </svg:g>
    </svg:g>
    <BLANKLINE>