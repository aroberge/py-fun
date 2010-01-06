''' mandel3.py

Mandelbrot set drawn in black and white.'''

import time  # (a)

import sys
if sys.version_info > (3,):
    import tkinter as tk
else:
    import Tkinter as tk
    range = xrange

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
    def __init__(self, parent, width=500, height=500,
                 min_x=-2.5, min_y=-2.5, max_x=2.5, max_y=2.5):
        self.canvas = tk.Canvas(parent, width=width, height=height)

        self.canvas_width = width
        self.canvas_height = height

        # The following are drawing boundaries in the complex plane
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.adjust_aspect_ratio()
        self.calculate_pixel_size()

        self.canvas.pack()
        self.draw_fractal()

    def adjust_aspect_ratio(self):
        '''ensures that min/max values in complex plane match aspect ratio
        of drawing canvas'''
        aspect_ratio = 1.0*self.canvas_width/self.canvas_height
        plane_width = self.max_x - self.min_x
        plane_height = self.max_y - self.min_y
        if 1.0*plane_width/plane_height < aspect_ratio:
            self.max_x = self.min_x + plane_height*aspect_ratio
        elif 1.0*plane_width/plane_height > aspect_ratio:
            self.max_y = self.min_y + plane_width/aspect_ratio
        else:
            pass

    def calculate_pixel_size(self):
        '''calculates the horizontal and vertical size of a pixel in
           complex plane coordinates'''
        self.delta_x = 1.*(self.max_x - self.min_x)/self.canvas_width
        self.delta_y = 1.*(self.max_y - self.min_y)/self.canvas_height

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
        for y in range(0, self.canvas_height):
            y_values.append(self.canvas_to_complex_plane_y(y))

        for x in range(0, self.canvas_width):
            real = self.canvas_to_complex_plane_x(x)
            for y in range(0, self.canvas_height):
                imag = y_values[y]
                c = complex(real, imag)
                if mandel(c):
                    self.draw_pixel(x, y)
        print("Time taken for calculating and drawing = %s" % (time.time() - begin))  # (a)

if __name__ == "__main__":
    root = tk.Tk()
    app = Viewer(root)
    root.mainloop()