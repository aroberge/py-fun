'''graphics2d.py

Basic opengl graphics shapes.
'''

from pyglet.gl import *



def draw_line(x1, y1, x2, y2, color=(1.0, 1.0, 1.0, 1.0), line_width=1):
    '''draw a line from (x1, y1) to (x2, y2) in the specified color
    '''
    glLineWidth(line_width)
    glBegin(GL_LINES)
    glColor4f(*color)
    glVertex2i(x1, y1)
    glVertex2i(x2, y2)
    glEnd()
    if line_width != 1:  # reset to default
        glLineWidth(1)

def draw_rect(x, y, width, height, color=(1.0, 1.0, 1.0, 1.0),
            filled=True, line_width=1):
    '''draw a rectangle starting at (x, y) with width and height given
       in the specified color.
    '''
    if filled:
        glBegin(GL_QUADS)
    else:
        glLineWidth(line_width)
        glBegin(GL_LINE_LOOP)
    glColor4f(*color)
    glVertex2i(x, y)
    glVertex2i(x + width, y)
    glVertex2i(x + width, y + height)
    glVertex2i(x, y + height)
    glEnd()
    if not filled and line_width != 1:  # reset to default
        glLineWidth(1)

if __name__ == '__main__':
    from pyglet import window
    from pyglet import clock
    from pyglet.window import key

    win = window.Window(640, 480, vsync=False)
    fps_display = clock.ClockDisplay()

    while not win.has_exit:

        win.dispatch_events()
        clock.tick()
        win.clear()
        color = (0, 1.0, 0, 0)
        draw_line(10, 10, 300, 200, color)
        color = (1.0, 1.0, 0, 0)
        draw_line(10, 30, 300, 370, color, line_width=5)
        color = (1.0, 0, 0, 0)
        draw_rect(200, 100, 50, 75, color)
        color = (0, 0, 1.0, 0)
        draw_rect(300, 100, 50, 75, color, filled=False)
        color = (0, 1.0, 1.0, 0)
        draw_rect(300, 100, 50, 75, color, filled=False, line_width=3)
        fps_display.draw()
        win.flip()