''' mandel9.py'''

import pyximport
pyximport.install()

from mandelbrot4 import create_fractal
from viewer import Viewer
import time

import sys
if sys.version_info > (3,):
    import tkinter as tk
else:
    import Tkinter as tk

class FancyViewer(Viewer):
    '''Window to display fractals'''

    def draw_fractal(self):
        '''draws a fractal on the canvas'''
        self.calculating = True
        begin = time.time()
        cols = create_fractal(self.canvas_width, self.canvas_height,
                              self.min_x, self.min_y,
                              self.delta_x, self.delta_y)
        self.image.put(cols)
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
        self.status.config(text=
                           "Time taken for calculating and drawing = %s    %s" %
                                        ((time.time() - begin), self.zoom_info))
        self.status2.config(text=self.info())
        #self.status2.update_idletasks()
        self.calculating = False


if __name__ == "__main__":
    root = tk.Tk()
    app = FancyViewer(root)
    root.mainloop()