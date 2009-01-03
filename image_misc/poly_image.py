'''
Application to approximate an image by a set of polygons.

Inspired by:
http://rogeralsing.com/2008/12/07/genetic-programming-evolution-of-mona-lisa/
'''

from random import randint
import time
import copy

import Tkinter as tk
import tkFileDialog, tkMessageBox
import Image, ImageTk, ImageChops, ImageStat # from PIL
import aggdraw

from state_engine import StateEngine

FITNESS_OFFSET = 0

# todo: investigate the use of ImageStat.Stat(image, mask)
# todo: investigate the use of stat.mean instead of stat.rms

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
        self.genes = []
        self.init_dna()

    def init_dna(self):
        for i in range(self.polygons):
            self.genes.append(self.create_random_polygon())

    def create_random_polygon(self):
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
            #choice = self.dna[selected][1][col_index]
            #choice = int(0.7*choice + 0.301*randint(0, 255))
            #self.dna[selected][1][col_index] = choice
            self.genes[selected][1][col_index] = randint(0, 255)
        elif _type == 1: # x coordinate
            coord = randint(0, self.edges-1)
            #choice = self.dna[selected][0][2*coord]
            #choice = int(0.7*choice + 0.301*randint(0, self.width))
            #self.dna[selected][0][2*coord] = choice
            self.genes[selected][0][2*coord] = randint(0, self.width)
        elif _type == 2: # y coordinate
            coord = randint(0, self.edges-1)
            #choice = self.dna[selected][0][2*coord+1]
            #choice = int(0.7*choice + 0.301*randint(0, self.height))
            #self.dna[selected][0][2*coord+1] = choice
            self.genes[selected][0][2*coord+1] = randint(0, self.height)

class AggDrawCanvas(tk.Canvas):
    def __init__(self, parent, original):
        tk.Canvas.__init__(self, parent)
        self.image_id = None
        self.img = None
        self.display_every = 1
        self.background = (0, 0, 0)

    def new_original(self, original):
        self.original = original
        self.mutations = 0
        _img = ImageTk.PhotoImage(self.original)
        self.set_size(_img.width(), _img.height())
        self.img = Image.new("RGBA", self._size, "black")
        self.dna = DNA(self._width, self._height)
        self.context = aggdraw.Draw(self.img)

    def set_size(self, width, height):
        self._width = width
        self._height = height
        self._size = width, height
        self.config(width=width, height=height+20)
        self.info = self.create_text(width/2, height+20)

    def draw_dna(self):
        brush = aggdraw.Brush(self.background, opacity=255)
        self.context.rectangle((0, 0, self._width, self._height), brush)
        for gene in self.dna.genes:
            brush = aggdraw.Brush(tuple(gene[1][0:3]), opacity=gene[1][3])
            self.context.polygon(gene[0], brush)
        self.redraw()

    def redraw(self):
        self.mutations += 1
        s = self.context.tostring()
        raw = Image.fromstring('RGBA', self._size, s)
        self.fitness = fitness(self.original, raw)
        if self.mutations % self.display_every:
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
        parent.controls = self

        # Main window
        filename_button = tk.Button(parent, text="New image",
                                    command=self.load_image)
        filename_button.pack(side=tk.TOP)
        self.original_image = tk.Canvas(parent)
        self.original_image.pack(side=tk.TOP)

        self.original = None
        # Best fit window
        self.best_fit_window = tk.Toplevel()
        self.best_fit_window.title("Current best fit.")
        self.best_fit = AggDrawCanvas(self.best_fit_window, self.original)
        self.best_fit.pack()

        # Current fit window
        cur_fit_window = tk.Toplevel()
        cur_fit_window.title("Current fit trial")
        self.current_fit = AggDrawCanvas(cur_fit_window, self.original)
        self.current_fit.pack()

        def prevent_accidental_closure():
            """prevents accidental closure of "child" window"""
            tkMessageBox.showinfo("Quit?",
                "Use the main window (where images are loaded) to end this program.")
        self.best_fit_window.protocol("WM_DELETE_WINDOW", prevent_accidental_closure)
        cur_fit_window.protocol("WM_DELETE_WINDOW", prevent_accidental_closure)

    def load_image(self):
        filename = tkFileDialog.askopenfilename()
        self.original = Image.open(filename)
        img = ImageTk.PhotoImage(self.original)
        self._width, self._height = width, height = img.width(), img.height()
        self.original_image.config(width=width, height=height)
        self.original_image.create_image(width/2, height/2, image=img)
        self.__img = img  # need to keep a reference otherwise it disappears!
        self.best_fit.new_original(self.original)
        self.best_fit.fitness = -1
        self.current_fit.new_original(self.original)

    def reset(self):
        '''restarts the image fitting with a new set of polygons'''
        self.running = False
        if tkMessageBox.askokcancel("",
                "New starting set of polygons?\nNote: you will lose all changes done so far."):
            self.best_fit.dna.init_dna()
            self.best_fit.mutations = 0
            self.best_fit.draw_dna()
            self.current_fit.dna.genes = self.best_fit.dna.genes
            self.current_fit.mutations = 0
            self.current_fit.draw_dna()

    def run(self):
        '''starts or resume/restarts the "fitting".'''
        self.running = True
        while self.running:
            done = self.step()
        return done

    def step(self):
        '''single mutation step; currently never ends on its own'''
        self.current_fit.dna.mutate()
        self.current_fit.draw_dna()
        if self.current_fit.fitness > self.best_fit.fitness:
            self.best_fit.dna.genes = copy.deepcopy(self.current_fit.dna.genes)
            self.best_fit.draw_dna()
        else:
            self.current_fit.dna.genes = copy.deepcopy(self.best_fit.dna.genes)
        return False # would return True to end the simulation

    def pause(self):
        '''self explanatory'''
        self.running = False

if __name__  == "__main__":
    main_app = tk.Tk()
    main_app.title('Image approximation with polygons')
    main_window = App(main_app)
    StateEngine(main_app, main_window.best_fit_window)
    main_app.mainloop()
