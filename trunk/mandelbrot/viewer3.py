# viewer3.py

import pyximport
pyximport.install()

from mandel3c_cy import create_fractal
from viewer import Viewer
import time

import sys
if sys.version_info < (3,):
    import Tkinter as tk
    range = xrange
else:
    import tkinter as tk

class FancyViewer(Viewer):
    '''Application to display fractals'''

    def draw_pixel(self, x, y):
        '''Simulates drawing a given pixel in black by drawing a black line
           of length equal to one pixel.'''
        self.canvas.create_line(x, y, x+1, y, fill="black")

    def draw_fractal(self):
        '''draws a fractal on the canvas'''
        self.calculating = True
        begin = time.time()
        self.canvas.create_rectangle(0, 0, self.canvas_width,
                                    self.canvas_height, fill="white")
        create_fractal(self.canvas_width, self.canvas_height,
                       self.min_x, self.min_y, self.max_x, self.max_y,
                       self.delta_x, self.delta_y, self.canvas)
        self.status.config(text=
                           "Time taken for calculating and drawing = %s    %s" %
                                        ((time.time() - begin), self.zoom_info))
        self.status2.config(text=self.info())
        self.calculating = False

if __name__ == "__main__":
    root = tk.Tk()
    app = FancyViewer(root)
    root.mainloop()