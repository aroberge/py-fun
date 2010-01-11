# viewer1.py

from mandel1c import mandel
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
        return
        self.canvas.create_line(x, y, x+1, y, fill="black")

    def draw_fractal(self):
        '''draws a fractal on the canvas'''
        self.calculating = True
        begin = time.time()
        # clear the canvas
        self.canvas.create_rectangle(0, 0, self.canvas_width,
                                    self.canvas_height, fill="white")
        for x in range(0, self.canvas_width):
            real = self.min_x + x*self.delta_x
            for y in range(0, self.canvas_height):
                imag = self.min_y + y*self.delta_y
                c = complex(real, imag)
                if mandel(c):
                    self.draw_pixel(x, self.canvas_height - y)
        self.status.config(text=
                           "Time taken for calculating and drawing = %s    %s" %
                                        ((time.time() - begin), self.zoom_info))
        self.status2.config(text=self.info())
        self.status2.update_idletasks()
        self.calculating = False

if __name__ == "__main__":
    root = tk.Tk()
    app = FancyViewer(root)
    root.mainloop()