''' mandel3.py

Mandelbrot set drawn in black and white.'''


import pyximport
pyximport.install()

from mandelbrot2 import mandel, create_fractal

import time  # (a)

import sys
if sys.version_info > (3,):
    import tkinter as tk
else:
    import Tkinter as tk
    range = xrange

class Viewer(object):
    '''Defines a widget to display fractals'''

    def __init__(self, parent, width=500, height=500,
                 min_x=-2.5, min_y=-2.5, max_x=2.5, max_y=2.5):

        self.parent = parent
        self.canvas_width = width
        self.canvas_height = height

        # The following are drawing boundaries in the complex plane
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

        self.calculate_pixel_size()
        self.calculating = False
        self.zoom_in_scale = 0.1
        self.zoom_out_scale = -0.125
        self.move_view_scale = 0.01

        self.parent.bind("+", self.zoom_in)
        self.parent.bind("-", self.zoom_out)
        self.parent.bind("<Up>", self.up)
        self.parent.bind("<Down>", self.down)
        self.parent.bind("<Left>", self.left)
        self.parent.bind("<Right>", self.right)

        self.canvas = tk.Canvas(parent, width=width, height=height)
        self.canvas.pack()
        self.status = tk.Label(self.parent, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        self.image = tk.PhotoImage(width=width, height=height)

        self.draw_fractal()

    def calculate_pixel_size(self):
        '''Calculates the horizontal and vertical size of a pixel in
           complex plane coordinates'''
        self.delta_x = 1.*(self.max_x - self.min_x)/self.canvas_width
        self.delta_y = 1.*(self.max_y - self.min_y)/self.canvas_height
        return

    def zoom_in(self, event):
        '''decreases the size of the region of the complex plane displayed'''
        if self.calculating:
            return
        self.status.config(text="Zooming in.  Please wait.")
        self.status.update_idletasks()
        self.change_scale(self.zoom_in_scale)

    def zoom_out(self, event):
        '''increases the size of the region of the complex plane displayed'''
        if self.calculating:
            return
        self.status.config(text="Zooming out.  Please wait.")
        self.status.update_idletasks()
        self.change_scale(self.zoom_out_scale)

    def change_scale(self, scale):
        '''changes the size of the region of the complex plane displayed and
           redraws'''
        if self.calculating:
            return
        dx = (self.max_x - self.min_x)*scale
        dy = (self.max_y - self.min_y)*scale
        self.min_x += dx
        self.max_x -= dx
        self.min_y += dy
        self.max_y -= dy
        self.calculate_pixel_size()
        self.draw_fractal()

    def left(self, event):
        '''shift the fractal drawing horizontally left'''
        if self.calculating:
            return
        self.status.config(text="Shifting left.  Please wait.")
        self.status.update_idletasks()
        dx = (self.max_x - self.min_x)*self.move_view_scale
        self.min_x += dx
        self.max_x += dx
        self.draw_fractal()

    def right(self, event):
        '''shift the fractal drawing horizontally right'''
        if self.calculating:
            return
        self.status.config(text="Shifting right.  Please wait.")
        self.status.update_idletasks()
        dx = (self.max_x - self.min_x)*self.move_view_scale
        self.min_x -= dx
        self.max_x -= dx
        self.draw_fractal()

    def up(self, event):
        '''shift the fractal drawing vertically up'''
        if self.calculating:
            return
        self.status.config(text="Shifting up.  Please wait.")
        self.status.update_idletasks()
        dy = (self.max_y - self.min_y)*self.move_view_scale
        self.min_y += dy
        self.max_y += dy
        self.draw_fractal()

    def down(self, event):
        '''shift the fractal drawing vertically down'''
        if self.calculating:
            return
        self.status.config(text="Shifting down.  Please wait.")
        self.status.update_idletasks()
        dy = (self.max_y - self.min_y)*self.move_view_scale
        # remember that canvas y coordinates are inverted
        self.min_y -= dy
        self.max_y -= dy
        self.draw_fractal()

    def clear(self):
        '''clears the canvas'''
        self.image.blank()

    def canvas_to_complex_plane_x(self, x):
        '''converts canvas coordinate into coordinate
           in the complex plane.'''
        return x*self.delta_x + self.min_x

    def canvas_to_complex_plane_y(self, y):
        '''converts canvas coordinate into coordinate
           in the complex plane.'''
        return (self.canvas_height - y)*self.delta_y + self.min_y

    def complex_plane_to_canvas_x(self, x):
        '''converts complex plane coordinate into coordinate on the canvas.'''
        return int((x - self.min_x)/self.delta_x)

    def complex_plane_to_canvas_y(self, y):
        '''converts complex plane coordinate into coordinate on the canvas.'''
        return int((y - self.min_y)/self.delta_y + self.canvas_height)


    def draw_fractal(self):
        '''draws a fractal on the canvas'''
        self.calculating = True
        #self.image.blank()
        begin = time.time()  # (a)

        cols = create_fractal(self.canvas_width, self.canvas_height,
                              self.min_x, self.min_y,
                              self.delta_x, self.delta_y)

        self.image.put(cols)
        self.canvas.create_image(0, 0, image = self.image, anchor=tk.NW)
        self.status.config(text="Time taken for calculating and drawing = %s" %
                                            (time.time() - begin))  # (a)
        self.calculating = False


if __name__ == "__main__":
    root = tk.Tk()
    app = Viewer(root)
    root.mainloop()