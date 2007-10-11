'''graphics2d.py

Basic 2d graphics shapes to use with pyglet/opengl.

To make use of some of the advanced options (for example, line stippling),
one must be familiar with the opengl documentation.
'''
from pyglet.gl import *

__all__ = ["draw_arc", "draw_circle", "draw_line", "draw_rect", "draw_ring",
           "Arc", "Circle", "Line", "Rect", "Ring"]

def draw_line(x1, y1, x2, y2, color=(1.0, 1.0, 1.0, 1.0), line_width=1,
    line_stipple=False):
    '''draws a line from (x1, y1) to (x2, y2).

        Note: line_stipple, which has a default value of False, needs to be
        specified as a 2-tuple (factor and stipple pattern e.g. 0x00FF)

    '''
    glLineWidth(line_width)
    if line_stipple:
        glLineStipple(*line_stipple)
        glEnable(GL_LINE_STIPPLE)
    glBegin(GL_LINES)
    glColor4f(*color)
    glVertex2i(int(x1), int(y1))
    glVertex2i(int(x2), int(y2))
    glEnd()
    if line_width != 1:  # reset to default
        glLineWidth(1)
    if line_stipple:
        glDisable(GL_LINE_STIPPLE)

def draw_rect(x, y, width, height, color=(1.0, 1.0, 1.0, 1.0),
            filled=True, line_width=1):
    '''draws a rectangle starting at (x, y) with width and height specified.

       Note: line_width is only relevant if filled==False.

    '''

    if filled:
        glBegin(GL_QUADS)
    else:
        glLineWidth(line_width)
        glBegin(GL_LINE_LOOP)
    glColor4f(*color)
    glVertex2i(int(x), int(y))
    glVertex2i(int(x + width), int(y))
    glVertex2i(int(x + width), int(y + height))
    glVertex2i(int(x), int(y + height))
    glEnd()
    if not filled and line_width != 1:  # reset to default
        glLineWidth(1)

def draw_circle(x, y, r, color=(1.0, 1.0, 1.0, 1.0)):
    '''draws a circle of radius r centered at (x, y)'''
    draw_ring(x, y, 0, r, color)

def draw_ring(x, y, inner, outer, color=(1.0, 1.0, 1.0, 1.0)):
    '''draws a ring of inner radius "inner" and outer radius "outer"
       centered at (x, y).

    '''
    glPushMatrix()
    glColor4f(*color)
    glTranslatef(x, y, 0)
    q = gluNewQuadric()
    # a circle is written as a number of triangular slices; we use
    # a maximum of 360 which looked smooth even for a circle as
    # large as 1500 px.
    # Smaller circles can be drawn with fewer slices - the rule we
    # use amount to approximately 1 slice per px on the circumference
    slices = min(360, 6*outer)
    gluDisk(q, inner, outer, slices, 1)
    glPopMatrix()

def draw_arc(x, y, inner, outer, start=0, sweep=180, color=(1.0, 1.0, 1.0, 1.0)):
    '''draws an arc of circle of inner radius "inner" and outer radius "outer"
       centered at (x, y).   The arc will start at a value "start" which is
       specified in degrees as measured counterclockwise starting from the
       x-axis and will "sweep" over a specified angle measured in degrees.

    '''
    glPushMatrix()
    glColor4f(*color)
    glTranslatef(x, y, 0)
    q = gluNewQuadric()
    # a circle is written as a number of triangular slices; we use
    # a maximum of 360 which looked smooth even for a circle as
    # large as 1500 px.
    # Smaller circles can be drawn with fewer slices - the rule we
    # use amount to approximately 1 slice per px on the circumference
    slices = min(360, 6*outer)
    # the opengl convention is to start on the +y axis in the clockwise
    # direction; we follow the mathematical notation, starting on the
    # +x axis, in the counterclockwise direction
    gluPartialDisk(q, inner, outer, slices, 1, 90-start, -sweep)
    glPopMatrix()

# to do
##draw_polygon
##create classes corresponding to each graphical object

class GraphicalObject(object):
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Rect(GraphicalObject):
    def __init__(self, x, y, width, height, color=(1.0, 1.0, 1.0, 1.0),
                 filled=True, line_width=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.filled = filled
        self.line_width = line_width

    def draw(self):
        draw_rect(self.x, self.y, self.width, self.height,
                  self.color, self.filled, self.line_width)

class Circle(GraphicalObject):
    def __init__(self, x, y, r, color=(1.0, 1.0, 1.0, 1.0)):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self):
        draw_circle(self.x, self.y, self.r, self.color)

class Ring(GraphicalObject):
    def __init__(self, x, y, inner, outer, color=(1.0, 1.0, 1.0, 1.0)):
        self.x = x
        self.y = y
        self.inner = inner
        self.outer = outer
        self.color = color

    def draw(self):
        draw_ring(self.x, self.y, self.inner, self.outer, self.color)

class Arc(GraphicalObject):
    def __init__(self, x, y, inner, outer, start=0, sweep=180,
                color=(1.0, 1.0, 1.0, 1.0)):
        self.x = x
        self.y = y
        self.inner = inner
        self.outer = outer
        self.start = start
        self.sweep = sweep
        self.color = color

    def draw(self):
        draw_arc(self.x, self.y, self.inner, self.outer, self.start,
                 self.sweep, self.color)

    def rotate(self, a):
        self.start += a

# the following does not really need to derive from GraphicalObject
# since it overrides the only common method included so far.
class Line(GraphicalObject):

    def __init__(self, x1, y1, x2, y2, color=(1.0, 1.0, 1.0, 1.0),
                 line_width=1, line_stipple=False):
        '''Creates a line a line object from (x1, y1) to (x2, y2).

            Note: line_stipple, which has a default value of False, needs to be
            specified as a 2-tuple (factor and stipple pattern e.g. 0x00FF)

        '''
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.line_width = line_width
        self.line_stipple = line_stipple

    def move(self, dx, dy):
        self.x1 += dx
        self.x2 += dx
        self.y1 += dy
        self.y2 += dy

    def draw(self):
        draw_line(self.x1, self.y1, self.x2, self.y2, self.color,
                  self.line_width, self.line_stipple)

if __name__ == '__main__':
    from pyglet import window
    from pyglet import clock

    win = window.Window(800, 600)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    fps_display = clock.ClockDisplay()
    clock.set_fps_limit(60)
    rectangle = Rect(0, 0, 100, 100)
    arc = Arc(500, 100, 30, 80)

    while not win.has_exit:
        win.dispatch_events()
        clock.tick()
        win.clear()
        draw_line(0, 0, 300, 300)
        color = (0, 1.0, 0, 1)
        draw_line(10, 10, 300, 200, color)
        color = (1.0, 1.0, 0, 1)
        draw_line(10, 30, 300, 370, color, line_width=5, line_stipple=(3, 0x0C0F))
        color = (1.0, 0, 0, 0.5)
        draw_rect(200, 100, 50, 75, color)
        color = (0, 0, 1.0, 1)
        draw_rect(300, 100, 50, 75, color, filled=False)
        color = (0, 1.0, 1.0, 1)
        draw_rect(300, 100, 50, 75, color, filled=False, line_width=3)
        color = (1, 1, 1, 0.5)
        draw_circle(200, 200, 50, color)
        draw_circle(260, 200, 5)
        color = (1.0, 0, 1.0, 1.0)
        draw_circle(200, 260, 10, color)
        draw_arc(400, 100, 30, 80, 45, 135)
        arc.rotate(1)
        arc.draw()

        draw_ring(400, 300, 50, 70)
        rectangle.move(0.5, 0.5)
        rectangle.draw()
        fps_display.draw()

        win.flip()