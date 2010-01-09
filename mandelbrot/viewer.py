''' viewer.py

Base class viewer for fractals.'''

import sys
if sys.version_info > (3,):
    import tkinter as tk
else:
    import Tkinter as tk

class Viewer(object):
    '''Window to display fractals'''

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
        self.normal_zoom(None)

        self.canvas = tk.Canvas(parent, width=width, height=height)
        self.canvas.pack()
        self.status = tk.Label(self.parent, text="", bd=1, relief=tk.SUNKEN,
                               anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        self.status2 = tk.Label(self.parent, text=self.info(), bd=1,
                                relief=tk.SUNKEN, anchor=tk.W)
        self.status2.pack(side=tk.BOTTOM, fill=tk.X)
        self.image = tk.PhotoImage(width=width, height=height)

        # We change the size of the image using the keyboard.
        self.parent.bind("+", self.zoom_in)
        self.parent.bind("-", self.zoom_out)
        self.parent.bind("n", self.normal_zoom)
        self.parent.bind("b", self.bigger_zoom)

        # We move the canvas using the mouse.
        self.translation_line = None
        self.parent.bind("<Button-1>", self.mouse_down)
        self.parent.bind("<Button1-Motion>", self.mouse_motion)
        self.parent.bind("<Button1-ButtonRelease>", self.mouse_up)

        self.draw_fractal()  # Needs to be implemented by subclass

    def info(self):
        '''information about fractal location'''
        return "Location: (%f, %f) to (%f, %f)" %(self.min_x, self.min_y,
                                                  self.max_x, self.max_y)

    def calculate_pixel_size(self):
        '''Calculates the horizontal and vertical size of a pixel in
           complex plane coordinates'''
        self.delta_x = 1.*(self.max_x - self.min_x)/self.canvas_width
        self.delta_y = 1.*(self.max_y - self.min_y)/self.canvas_height
        return

    def mouse_down(self, event):
        '''records the x and y positions of the mouse when the left button
           is clicked.'''
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def mouse_motion(self, event):
        '''keep track of the mouse motion by drawing a line from its
           starting point to the current point.'''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        if (self.start_x != event.x)  and (self.start_y != event.y) :
            self.canvas.delete(self.translation_line)
            self.translation_line = self.canvas.create_line(
                                self.start_x, self.start_y, x, y, fill="orange")
            self.canvas.update_idletasks()

    def mouse_up(self, event):
        '''Moves the canvas based on the mouse motion'''
        dx = (self.start_x - event.x)*self.delta_x
        dy = (self.start_y - event.y)*self.delta_y
        self.min_x += dx
        self.max_x += dx
        # y-coordinate in complex plane run in opposite direction from
        # screen coordinates
        self.min_y -= dy
        self.max_y -= dy
        self.canvas.delete(self.translation_line)
        self.status.config(text="Moving the fractal.  Please wait.")
        self.status.update_idletasks()
        self.status2.config(text=self.info())
        self.status2.update_idletasks()
        self.draw_fractal()

    def normal_zoom(self, event, scale=1):
        '''Sets the zooming in/out scale to its normal value'''
        if scale==1:
            self.zoom_info = "[Normal zoom]"
        else:
            self.zoom_info = "[Faster zoom]"
        if event is not None:
            self.status.config(text=self.zoom_info)
            self.status.update_idletasks()
        self.zoom_in_scale = 0.1
        self.zoom_out_scale = -0.125

    def bigger_zoom(self, event):
        '''Increases the zooming in/out scale from its normal value'''
        self.normal_zoom(event, scale=3)
        self.zoom_in_scale = 0.3
        self.zoom_out_scale = -0.4

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

    def draw_fractal(self):
        '''draws a fractal on the canvas'''
        raise NotImplementedError

if __name__ == "__main__":
    root = tk.Tk()
    app = Viewer(root)
    root.mainloop()