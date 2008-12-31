#
# Tkinter 3000
#
# a simple agg-based drawing canvas
#

try:
    import aggdraw
except ImportError:
    print
    print "===", "this demo requires the aggdraw library"
    print "===", "see http://effbot.org/zone/aggdraw.htm"
    print
    raise

from WCK import *

import os, sys, time

from math import *

class AggCanvas(EventMixin, Widget):

    ui_option_width = 100
    ui_option_height = 100

    def ui_handle_config(self):
        return int(self.ui_option_width), int(self.ui_option_height)

    def ui_handle_resize(self, width, height):
        self.image = None
        self.size = width, height

    def ui_handle_clear(self, draw, x0, y0, x1, y1):
        pass

    def ui_handle_repair(self, draw, x0, y0, x1, y1):
        if not self.image:
            ink = self.winfo_rgb(self.ui_option_background)
            ink = "#%02x%02x%02x" % (ink[0]/256, ink[1]/256, ink[2]/256)
            try:
                # see if we can use a Dib surface (currently windows only)
                d = aggdraw.Dib("RGB", self.size, ink)
                self.agg_repair(d)
                self.image = d
                self.expose = 1 # use expose to update window
            except (AttributeError, ValueError):
                # use a traditional aggdraw surface
                d = aggdraw.Draw("RGB", self.size, ink)
                self.agg_repair(d)
                self.image = self.ui_image(d.mode, d.size, d.tostring())
                self.expose = 0
        if self.expose:
            self.image.expose(self.winfo_id())
        else:
            draw.paste(self.image)

    def agg_damage(self, *extent):
        self.image = None
        self.ui_damage(*extent)

    def agg_repair(self, draw):
        pass

def color((r, g, b)):
    r = min(255 * r, 255)
    g = min(255 * g, 255)
    b = min(255 * b, 255)
    return "#%02x%02x%02x" % (r, g, b)

SHADE = 0.2
def golden_section(draw, size):
    # "golden section", adapted from a DrawBot demo script
    # (see http://just.letterror.com/ltrwiki/DrawBot)
    w, h = size
    cx, cy = w/2, h/2
    s = min(w / 400.0, h / 400.0)
    phi = (sqrt(5) + 1)/2-1
    oradius = 10.0
    for i in range(720):
        c = (0.0, 0.0, 0.0)
        r = s * 1.5*oradius * sin(i * pi/720)
        x = cx + s*0.25*i*cos(phi*i*2*pi)
        y = cy + s*0.25*i*sin(phi*i*2*pi)
        draw.ellipse(
            (x-r/2, y-r/2, x+r/2, y+r/2), aggdraw.Brush(color(c))
            )
        c = i / 360.0, i / 360.0, SHADE
        r = s * oradius * sin(i * pi/720)

        draw.ellipse(
            (x-r/2, y-r/2, x+r/2, y+r/2), aggdraw.Brush(color(c))
            )

class MyCanvas(AggCanvas):
    def agg_repair(self, draw):
        golden_section(draw, self.size)
    def update(self):
        self.agg_damage(self.size)

if __name__ == "__main__":

    import Tkinter

    root = Tkinter.Tk()
    root.title("demoAggCanvas")

    widget = MyCanvas(root, width=500, height=500)
    widget.pack(fill="both", expand=1)
    for i in range(20):
        SHADE += 0.1
        print SHADE
        widget.update()
        time.sleep(0.1)

    root.mainloop()
