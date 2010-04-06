# viewer2b.py

import pyximport
pyximport.install()

from mandel2h_cy import create_fractal
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

    def draw_fractal(self):
        '''draws a fractal on the canvas'''
        self.calculating = True
        begin = time.time()
        # clear the canvas
        self.canvas.create_rectangle(0, 0, self.canvas_width,
                                    self.canvas_height, fill="white")
        create_fractal(self.canvas_width, self.canvas_height,
                       self.min_x, self.min_y, self.pixel_size,
                       self.nb_iterations, self.canvas)
        self.status.config(text="Time required = %.2f s  [%s iterations]  %s" %(
                                (time.time() - begin), self.nb_iterations,
                                                                self.zoom_info))
        self.status2.config(text=self.info())
        self.calculating = False

if __name__ == "__main__":
    root = tk.Tk()
    app = FancyViewer(root)
    root.mainloop()