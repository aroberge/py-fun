'''
Playing with images....
'''

#from Tkinter import Canvas, Tk, Label
import Tkinter as tk
import Image, ImageTk, ImageChops, ImageStat # PIL
import aggdraw
from random import randint
import time
import copy

FITNESS_OFFSET = 0
saved = [None, None]
def fitness(im1, im2):
    """Calculate a value derived from the root mean squared of the difference
    between two images.  It is normalized so that when a black image is
    compared with the original one (img1), the fitness given is 0, and when the
    image is identical, the fitness value is 100."""
    global FITNESS_OFFSET
    try:
        stat = ImageStat.Stat(ImageChops.difference(im1, im2))
    except:
        print "missing alpha channel in original image?"
        im1.putalpha(255)
        stat = ImageStat.Stat(ImageChops.difference(im1, im2))
    fit = 1. - sum(stat.rms[:3])/(255*3)
    if FITNESS_OFFSET == 0:
        black_image = aggdraw.Draw("RGBA", im1.size, "black")
        s = black_image.tostring()
        raw = Image.fromstring('RGBA', im1.size, s)
        stat = ImageStat.Stat(ImageChops.difference(im1, raw))
        FITNESS_OFFSET = 1. - sum(stat.rms[:3])/(255*3)
    return 100*(fit-FITNESS_OFFSET)/(1.-FITNESS_OFFSET)

class DNA(object):
    def __init__(self, width, height, polygons=50, edges=6):
        self.polygons = polygons
        self.edges = edges
        self.width = width
        self.height = height
        self.dna = []

    def init_dna(self):
        for i in range(self.polygons):
            self.dna.append(self.random_polygon())

    def random_polygon(self):
        edges = []
        for i in range(self.edges):
            edges.append(randint(0, self.width))
            edges.append(randint(0, self.height))
        col = [randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)]
        return edges, col

    def mutate(self):
        selected = randint(0, self.polygons-1)
        _type = randint(0, 2)
        if _type == 0: # colour
            col_index = randint(0, 3)
            self.dna[selected][1][col_index] += randint(0, 255)
            self.dna[selected][1][col_index] /= 2
        elif _type == 1: # x coordinate
            coord = randint(0, self.edges-1)
            self.dna[selected][0][2*coord] += randint(0, self.width)
            self.dna[selected][0][2*coord] /=2
        elif _type == 2: # y coordinate
            coord = randint(0, self.edges-1)
            self.dna[selected][0][2*coord+1] += randint(0, self.height)
            self.dna[selected][0][2*coord+1] /=2

class AggDrawCanvas(tk.Canvas):
    def __init__(self, width, height, win):
        tk.Canvas.__init__(self, win)
        self.image_id = None
        self.img = None
        self.win = win
        self._width = width
        self._height = height
        self._size = width, height
        self.config(width=width, height=height+20)
        self.info = self.create_text(width/2, height+20)
        self.dna = DNA(self._width, self._height)
        self.mutations = 0
        self.display_every = 1

    def draw_dna(self):
        if self.img is None:
            self.img = Image.new("RGBA", self._size, "black")
            self.context = aggdraw.Draw(self.img)
        else:
            brush = aggdraw.Brush((0, 0, 0), opacity=255)
            self.context.rectangle((0, 0, self._width, self._height), brush)
        for gene in self.dna.dna:
            brush = aggdraw.Brush(tuple(gene[1][0:3]), opacity=gene[1][3])
            self.context.polygon(gene[0], brush)
        self.redraw()

    def redraw(self):
        self.mutations += 1
        s = self.context.tostring()
        self.delete(self.context)
        raw = Image.fromstring('RGBA', self._size, s)
        self.fitness = fitness(mona_lisa, raw)
        if self.mutations % self.display_every: # display only every 10 images
            return
        self.itemconfig(self.info,
                        text="%2.2f  %d"%(self.fitness, self.mutations),
                        fill="black")
        self.image = ImageTk.PhotoImage(raw)
        self.delete(self.image_id)
        self.image_id = self.create_image(self._width/2, self._height/2, image=self.image)
        self.update()

class App(object):
    """The main application window"""
    def __init__(self, parent):
        frame = tk.Frame(parent)
        frame.pack()
        self.original_image = tk.Canvas(frame)
        self.original_image.pack(side=tk.LEFT)
        self.best_fit = AggDrawCanvas(frame)
        self.current_fit = AggDrawCanvas(frame)

    def load_image(self, filename):
        self.target_image = Image.open(filename)
        img = ImageTk.PhotoImage(self.target_image)
        width, height = img.width(), img.height()
        self.original_image.config(width=width, height=height)
        self.original_image.create_image(width/2, height/2, image=img)
        self.best_fit.set_size(width, height)
        self.current_fit.set_size(width, height)




#root = tk.Tk()
#
#app = App(root)
#
#root.mainloop()
#root.destroy() # optional; see description below

win = tk.Tk()

mona_lisa = Image.open("mona_lisa.png")
#mona_lisa = Image.open("mona.png")
img = ImageTk.PhotoImage(mona_lisa)

PAUSED = False
def key(event):
    print "pressed", repr(event.char)
    global PAUSED
    if event.char == 'p':
        PAUSED = not PAUSED
    print PAUSED

win.bind("<Key>", key)


original_image = tk.Canvas(win)
original_image.grid(row=0)
#fitness_label = Label(win)

_w, _h = img.width(), img.height()
original_image.config(width=_w, height=_h)
original_image.create_image(_w/2, _h/2, image=img)

best_fit = AggDrawCanvas(_w, _h, win)
best_fit.grid(row=1, column=0)
best_fit.dna.dna = []
best_fit.draw_dna()

current_fit = AggDrawCanvas(_w, _h, win)
current_fit.grid(row=1, column=1)
current_fit.display_every = 1 # 10
current_fit.dna.init_dna()
current_fit.draw_dna()

while True:
    while not PAUSED:
        current_fit.dna.mutate()
        current_fit.draw_dna()
        if current_fit.fitness > best_fit.fitness:
            best_fit.dna.dna = copy.deepcopy(current_fit.dna.dna)
            best_fit.draw_dna()
        else:
            current_fit.dna.dna = copy.deepcopy(best_fit.dna.dna)


if __name__ == '__main__':
    win.mainloop()