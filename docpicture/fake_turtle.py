"""
This is a fake turtle module (with no relevant executable code, other than
a local docpicture parser included for testing) obtained through
severely amputating the original turtle module, for the purpose of
demonstrating the docpicture concept.


Aside: just for a quick test, we include another type of object.
..docpicture:: websequence
  Alice->Bob: Authentication Request
  Bob-->Alice: Authentication Response


From the original:
====================

Turtle graphics is a popular way for introducing programming to
kids. It was part of the original Logo programming language developed
by Wally Feurzeig and Seymour Papert in 1966.

Imagine a robotic turtle starting at (0, 0) in the x-y plane. Give it
the command turtle.forward(15), and it moves (on-screen!) 15 pixels in
the direction it is facing, drawing a line as it moves. Give it the
command turtle.left(25), and it rotates in-place 25 degrees clockwise.

By combining together these and similar commands, intricate shapes and
pictures can easily be drawn.
=====================

For docpictures, we modify slightly the notation so as to include
the angle at which the turtle is rotated.  For example, we could have

..docpicture:: bw_turtle
   turtle(20).forward(125)

We also have some other styles available, such as

..docpicture:: color_turtle
   turtle.down()
   turtle(20).forward(125)

and even

..docpicture:: turtle
   turtle.down()
   turtle.color("red")
   turtle(20).forward(125)

As an additional test, we include a drawing made with a docpicture "parser"
that is not part of the normal docpicture distribution, but is
defined in this file. We *suggest* that such parser names start
with "self." to indicate to the reader that they are defined locally.
docpicture will handle any name - but will first look for names in
its normal set.

..docpicture:: self.red_turtle
   turtle.down()
   turtle.color("green")
   turtle(45).forward(200)

Finally, we include a drawing with an unknown docpicture object - no
drawing will be made.

..docpicture:: unknown
   turtle(20).forward(125)

"""

class RawPen:

    def forward(self, distance):
        """ Go forward distance steps.

        Example:
        >>> turtle.position()
        [0.0, 0.0]
        >>> turtle.forward(25)
        >>> turtle.position()
        [25.0, 0.0]
        >>> turtle.forward(-75)
        >>> turtle.position()
        [-50.0, 0.0]

        =====================
        Using docpicture.view, you can see something like this in picture.

        ..docpicture:: turtle
            turtle(0).forward(75)
        """
        pass

    def left(self, angle):
        """ Turn left angle units (units are by default degrees,
        but can be set via the degrees() and radians() functions.)

        When viewed from above, the turning happens in-place around
        its front tip.

        Example:
        >>> turtle.heading()
        22
        >>> turtle.left(45)
        >>> turtle.heading()
        67.0

        ================
        Using docpicture.view, you can see something like this in picture.
        ..docpicture:: turtle
          turtle(22).left(45)

        """
        pass

    def right(self, angle):
        """ Turn right angle units (units are by default degrees,
        but can be set via the degrees() and radians() functions.)

        When viewed from above, the turning happens in-place around
        its front tip.

        Example:
        >>> turtle.heading()
        22
        >>> turtle.right(45)
        >>> turtle.heading()
        337.0


        ================
        Using docpicture.view, you can see something like this in picture.
        ..docpicture:: turtle
          turtle(22).right(45)
        """
        pass

    def up(self):
        """ Pull the pen up -- no drawing when moving.

        Example:
        >>> turtle.up()

        ================
        Using docpicture.view, you can see something like this in picture.
        ..docpicture:: turtle
           turtle.up()
           turtle(10).forward(100)
        """
        pass

    def down(self):
        """ Put the pen down -- draw when moving.

        Example:
        >>> turtle.down()


        ================
        Let's add a picture
        ..docpicture:: turtle
           turtle.down()
           turtle(10).forward(100)

        """
        pass

    def color(self, *args):
        """ Set the pen color.

        In the original, three input formats are allowed; for docpicture,
        only the named color is supported.

            color(s)
            s is a Tk specification string, such as "red" or "yellow"


        Example:

        >>> turtle.color('brown')

        ================
        Using docpicture.view, you can see something like this in picture.
        ..docpicture:: turtle
           turtle.down()
           turtle.color("brown")
           turtle(10).forward(100)
        """
        pass
