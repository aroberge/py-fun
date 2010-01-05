''' mandel1.py

Mandelbrot set drawn in black and white.'''

import time  # (a)

import sys
if sys.version_info > (3,):
    import tkinter as tk
else:
    import Tkinter as tk
    range = xrange  # (b)

def mandel(c):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after 20 iterations, the absolute value of the resulting number is
       greater or equal to 2.'''
    z = 0
    for iter in range(0, 20):
        z = z**2 + c
        if abs(z) >= 2:
            return False
    return abs(z) < 2

class Viewer(object):
    def __init__(self, parent, width=500, height=500):
        self.canvas = tk.Canvas(parent, width=width, height=height)
        self.width = width
        self.height = height

        # the following "shift" variables are used to center the drawing
        self.shift_x = 0.5*self.width
        self.shift_y = 0.5*self.height
        self.scale = 0.01

        self.canvas.pack()
        self.draw_fractal()

    def screen_to_complex_plane(self, coordinate, shift):
        '''converts screen coordinate into coordinate
           in the complex plane.'''
        return (coordinate - shift)*self.scale

    def draw_pixel(self, x, y):
        '''Simulates drawing a given pixel in black by drawing a black line
           of length equal to one pixel.'''
        # technically, we should use "self.height - y" instead of "y" but,
        # since there is symmetry about the x-axis, we can use the simpler
        # expression.
        self.canvas.create_line(x, y, x+1, y, fill="black")

    def draw_fractal(self):
        begin = time.time()  # (a)
        y_values = []
        for y in range(0, self.height):
            y_values.append(self.screen_to_complex_plane(y, self.shift_y))

        for x in range(0, self.width):
            real = self.screen_to_complex_plane(x, self.shift_x)
            for y in range(0, self.height):
                imag = y_values[y]
                c = complex(real, imag)
                if mandel(c):
                    self.draw_pixel(x, y)
        print("Time taken for calculating and drawing = %s" % (time.time() - begin))  # (a)

if __name__ == "__main__":
    root = tk.Tk()
    app = Viewer(root)
    root.mainloop()