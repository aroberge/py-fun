''' mandel1.py

Mandelbrot set drawn in black and white.'''

#import time  # (a)

import sys
if sys.version_info > (3,):
    import tkinter as tk
else:
    import Tkinter as tk
    #range = xrange  # (b)

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
        self.scale = 0.01
        self.canvas.pack()
        self.draw_fractal()

    def x_screen_to_complex_plane(self, coordinate):
        '''converts horizontal screen coordinate into real coordinate
           in the complex plane.'''
        return (coordinate - 0.5*self.width)*self.scale

    def y_screen_to_complex_plane(self, coordinate):
        '''converts vertical screen coordinate into imaginary coordinate
           in the complex plane.'''
        return (coordinate - 0.5*self.height)*self.scale

    def draw_pixel(self, x, y):
        '''Simulates drawing a given pixel in black by drawing a black line
           of length equal to one pixel.'''
        # technically, we should use "self.height - y" instead of "y" but,
        # since there is symmetry about the x-axis, we can use the simpler
        # expression.
        self.canvas.create_line(x, y, x+1, y, fill="black")

    def draw_fractal(self):
    	#begin = time.time()  # (a)
        for x in range(0, self.width):
            real = self.x_screen_to_complex_plane(x)
            for y in range(0, self.height):
                imag = self.y_screen_to_complex_plane(y)
                c = complex(real, imag)
                if mandel(c):
                    self.draw_pixel(x, y)
        #print("Time taken for calculating and drawing = %s" % (time.time() - begin))  # (a)

if __name__ == "__main__":
    root = tk.Tk()
    app = Viewer(root)
    root.mainloop()