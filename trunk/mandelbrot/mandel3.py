''' mandel3.py

Mandelbrot set drawn in black and white.'''

import time  # (a)

import sys
if sys.version_info > (3,):
    import tkinter as tk
else:
    import Tkinter as tk
    range = xrange
    
def mandel(c, max_iter=20):
    '''determines if a point is in the Mandelbrot set based on deciding if,
       after a specified number of iterations (or 20 by default), 
       the absolute value of the resulting number is greater or equal to 2.'''
    z = 0
    for iter in range(0, max_iter):
        z = z**2 + c
        if abs(z) >= 2:
            return False
    return abs(z) < 2

class Viewer(object):
    def __init__(self, parent, width=500, height=500,
                 min_x=-2.5, min_y=-2.5, max_x=2.5, max_y=2.5):
        self.canvas = tk.Canvas(parent, width=width, height=height)
        self.parent = parent

        self.canvas_width = width
        self.canvas_height = height

        # The following are drawing boundaries in the complex plane
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.adjust_aspect_ratio()

        self.parent.bind("+", self.zoom_in)
        self.parent.bind("-", self.zoom_out)
        self.calculating = False
        self.canvas.pack()
        self.status = tk.Label(self.parent, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        self.draw_fractal()
        
    def adjust_aspect_ratio(self):
        '''ensures that min/max values in complex plane match aspect ratio
        of drawing canvas and calculate pixel sizes.'''
        aspect_ratio = 1.0*self.canvas_width/self.canvas_height
        plane_width = self.max_x - self.min_x
        plane_height = self.max_y - self.min_y
        if 1.0*plane_width/plane_height < aspect_ratio:
            self.max_x = self.min_x + plane_height*aspect_ratio
        elif 1.0*plane_width/plane_height > aspect_ratio:
            self.max_y = self.min_y + plane_width/aspect_ratio
        else:
            pass
        self.calculate_pixel_size()
        return

    def calculate_pixel_size(self):
        '''Calculates the horizontal and vertical size of a pixel in
           complex plane coordinates'''
        self.delta_x = 1.*(self.max_x - self.min_x)/self.canvas_width
        self.delta_y = 1.*(self.max_y - self.min_y)/self.canvas_height
        return     

    def zoom_in(self, event):
        if self.calculating:
            return
        self.status.config(text="Zooming in.  Please wait.")
        self.status.update_idletasks()
        self.change_scale(0.1)  # reduces the region of interest by 20%

    def zoom_out(self, event):
        if self.calculating:
            return
        self.status.config(text="Zooming out.  Please wait.")
        self.status.update_idletasks()
        self.change_scale(-0.125) # increases the region of interest by 25%

    def change_scale(self, scale):
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

    def clear(self):
        self.canvas.create_rectangle(0, 0, self.canvas_width, 
                                    self.canvas_height, fill="white")
        
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
        # The screen y coordinates run in opposite direction to that of the
        # complex plane.
        y = self.canvas_height - y
        self.canvas.create_line(x, y, x+1, y, fill="black")

    def draw_fractal(self):
        self.calculating = True
        self.clear()
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
        self.status.config(text="Time taken for calculating and drawing = %s" %
                                            (time.time() - begin))  # (a)
        self.calculating = False

        
if __name__ == "__main__":
    root = tk.Tk()
    app = Viewer(root)
    root.mainloop()