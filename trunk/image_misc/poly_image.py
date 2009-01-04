'''
Application to approximate an image by a set of polygons.

Inspired by:
http://rogeralsing.com/2008/12/07/genetic-programming-evolution-of-mona-lisa/
'''

from random import randint
import time
import copy

import Tkinter as tk
import tkFileDialog, tkMessageBox, tkSimpleDialog
import Image, ImageTk, ImageChops, ImageStat # from PIL
import aggdraw

from state_engine import StateEngine
from src.color_chooser import SimpleColorChooser

FITNESS_OFFSET = 0

# todo: investigate the use of ImageStat.Stat(image, mask)
# todo: investigate the use of stat.mean instead of stat.rms

def fitness(im1, im2, background="black"):
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
        black_image = aggdraw.Draw("RGBA", im1.size, background)
        s = black_image.tostring()
        raw = Image.fromstring('RGBA', im1.size, s)
        stat = ImageStat.Stat(ImageChops.difference(im1, raw))
        FITNESS_OFFSET = 1. - sum(stat.rms[:3])/(255*3)
    return 100*(fit-FITNESS_OFFSET)/(1.-FITNESS_OFFSET)

class DNA(object):
    def __init__(self, width, height, polygons=50, edges=6, background=(0, 0, 0)):
        self.polygons = polygons
        self.background = background
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
        return [edges, col]

    def mutate(self):
        selected = randint(0, self.polygons-1)
        _type = randint(0, 2)
        if _type == 0: # colour
            col_index = randint(0, 3)
            self.genes[selected][1][col_index] = randint(0, 255)
        elif _type == 1: # x coordinate
            coord = randint(0, self.edges-1)
            self.genes[selected][0][2*coord] = randint(0, self.width)
        elif _type == 2: # y coordinate
            coord = randint(0, self.edges-1)
            self.genes[selected][0][2*coord+1] = randint(0, self.height)

class AggDrawCanvas(tk.Canvas):
    def __init__(self, parent, original):
        tk.Canvas.__init__(self, parent)
        self.parent = parent
        self.image_id = None
        self.img = None
        self.display_every = 1
        self.background = "#000000"
        # the following are used to calculate the average nb of mutation/second
        self.keep_last_n = 20
        self.gen_times = [1. for i in range(self.keep_last_n)]
        self.last_time = time.time()

    def new_original(self, original):
        self.original = original
        self.mutations = 0
        _img = ImageTk.PhotoImage(self.original)
        self.set_size(_img.width(), _img.height())
        self.img = Image.new("RGBA", self.size_, self.background)
        self.dna = DNA(self.width_, self.height_, background=self.background)
        self.context = aggdraw.Draw(self.img)

    def set_size(self, width, height):
        self.width_ = width
        self.height_ = height
        self.size_ = width, height
        self.config(width=width, height=height)

    def draw_dna(self):
        brush = aggdraw.Brush(self.background, opacity=255)
        self.context.rectangle((0, 0, self.width_, self.height_), brush)
        for gene in self.dna.genes:
            brush = aggdraw.Brush(tuple(gene[1][0:3]), opacity=gene[1][3])
            self.context.polygon(gene[0], brush)
        self.redraw()

    def redraw(self):
        self.mutations += 1
        self.calc_average_time()
        s = self.context.tostring()
        raw = Image.fromstring('RGBA', self.size_, s)
        self.fitness = fitness(self.original, raw, self.background)
        if self.mutations % self.display_every:
            return
        self.parent.update_info()
        self.image = ImageTk.PhotoImage(raw)
        self.delete(self.image_id)
        self.image_id = self.create_image(self.width_/2, self.height_/2, image=self.image)
        self.update()

    def calc_average_time(self):
        '''calculates the average time for a given mutation - based on the
           previous "fastest n-1" and converts it to a number of mutation
           per second.'''
        now = time.time()
        self.gen_times[self.mutations%self.keep_last_n] = now - self.last_time
        self.last_time = now
        # discard the longest time iteration to avoid skewing results
        self.ave_gen_per_second = self.keep_last_n/sum(sorted(self.gen_times)[:-1])

def prevent_accidental_closure():
    """prevents accidental closure of "child" window"""
    tkMessageBox.showinfo("Quit?",
        "Use the main window (where images are loaded) to end this program.")

class ImageFrequency(tkSimpleDialog.Dialog):
    def body(self, parent):
        self.parent = parent
        tk.Label(parent, text="Select the image drawing frequency").pack()
        self.choice = tk.Entry(parent)
        self.choice.pack()
        return self.choice # initial focus

    def apply(self):
        self.result=self.choice.get()

class FitWindow(tk.Toplevel):
    def __init__(self, parent, original_image, title):
        tk.Toplevel.__init__(self)
        self.title(title)
        self.parent = parent
        main_frame = tk.Frame(self)
        # image frame
        self.image_frame = tk.Frame(main_frame)
        self.image_frame.update_info = self.update_info
        self.fit = AggDrawCanvas(self.image_frame, original_image)
        self.fit.pack()
        self.protocol("WM_DELETE_WINDOW", prevent_accidental_closure)
        info_frame = tk.Frame(self.image_frame)
        info_frame.pack()
        self.info = tk.Label(info_frame, text="Current fitness")
        self.info.pack()
        self.show_every_btn = tk.Button(info_frame, width=25, height=1,
                    text="Display every %d image." % self.fit.display_every,
                                         command=self.set_show_every)
        self.show_every_btn.pack()
        self.image_frame.pack(side=tk.LEFT)
        self.setup_controls(main_frame)
        main_frame.pack()

    def setup_controls(self, main_frame):
        pass   # implemented by subclass

    def update_info(self):
        if self.fit.ave_gen_per_second > 2:
            self.info.config(text = "Fitness: %2.2f\nMutations: %d\n[per second: %d]" %
                         (self.fit.fitness, self.fit.mutations,
                          int(self.fit.ave_gen_per_second)))
        else:
            self.info.config(text = "Fitness: %2.2f\nMutations: %d\n[per second: %1.2f]" %
                         (self.fit.fitness, self.fit.mutations,
                          self.fit.ave_gen_per_second))

    def set_show_every(self):
        set_frequency_dialog = ImageFrequency(self)
        try:
            self.fit.display_every = int(set_frequency_dialog.result)
            self.show_every_btn.config(text =
                            "Display every %d image.\n" % self.fit.display_every)
        except:
            tkMessageBox.showerror('', "Integer value required.")

class BestFitWindow(FitWindow):

    def setup_controls(self, main_frame):
        self.control_frame = tk.Frame(main_frame)
        set_color_btn = tk.Button(main_frame, width=25,
                                        text="Select background color",
                                        command=self.parent.set_background_color)
        set_color_btn.pack()
        self.color_value = tk.Label(main_frame)
        self.color_value.configure(text=self.fit.background)
        self.color_value.pack(fill=tk.X, padx=2, pady=2)
        self.color_sample = tk.Label(main_frame)
        self.color_sample.pack(fill=tk.BOTH, padx=2, pady=2)
        self.color_sample.configure(background=self.fit.background)
        save_polygons_btn = tk.Button(main_frame, width=25,
                                        text="Save polygons",
                                        command=self.save_poly)
        save_polygons_btn.pack()
        load_polygons_btn = tk.Button(main_frame, width=25,
                                        text="Load polygons",
                                        command=self.load_poly)
        load_polygons_btn.pack()
        self.control_frame.pack(side=tk.LEFT)


    def save_poly(self):
        filename = tkFileDialog.asksaveasfilename()
        if not filename:
            return
        filehandle = open(filename, "w")
        print "save_poly called"
        dna = []
        dna.append(self.fit.background)
        dna.append(str(self.fit.dna.polygons))
        dna.append(str(self.fit.dna.edges))
        coords = range(2*self.fit.dna.edges)
        for gene in self.fit.dna.genes:
            for item in gene:
                for value in item:
                    dna.append(str(value))
        filehandle.write(' '.join(dna))

    def load_poly(self):
        filename = tkFileDialog.askopenfilename()
        if not filename:
            return
        items = open(filename).read().split()
        self.fit.background = items[0]
        self.fit.dna.polygons = int(items[1])
        self.fit.dna.edges = int(items[2])
        nb_coords = 2*self.fit.dna.edges
        nb_subitems = nb_coords + 4  # 4 color values per polygon
        offset = 3  # first 3 values are excluded
        self.fit.dna.genes = []
        for i in range(self.fit.dna.polygons):
            coords = []
            color = []
            for j in range(nb_coords):
                coords.append(int(items[offset+i*nb_subitems + j]))
            for j in range(4):
                color.append(int(items[offset+i*nb_subitems + nb_coords + j]))
            self.fit.dna.genes.append([coords, color])
        self.fit.current_fit.background = self.fit.background
        self.fit.current_fit.dna.polygons = self.fit.dna.polygons
        self.fit.current_fit.dna.edges = self.fit.dna.edges
        self.fit.current_fit.dna = copy.deepcopy(self.fit.dna)

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
        self.best_fit_window = BestFitWindow(self, self.original, "Best fit")
        self.best_fit = self.best_fit_window.fit
        cur_fit_window = FitWindow(self, self.original, "Current attempt")
        self.current_fit = cur_fit_window.fit
        self.best_fit.current_fit = self.current_fit

    def load_image(self):
        filename = tkFileDialog.askopenfilename()
        if not filename:
            return
        try:
            self.original = Image.open(filename)
        except IOError:
            print "ignored IOError; most likely not an valid image file"
            return
        img = ImageTk.PhotoImage(self.original)
        width, height = img.width(), img.height()
        self.original_image.config(width=width, height=height)
        self.original_image.create_image(width/2, height/2, image=img)
        self.__img = img  # need to keep a reference otherwise it disappears!
        self.best_fit.new_original(self.original)
        self.best_fit.draw_dna()
        self.current_fit.new_original(self.original)
        self.current_fit.dna = copy.deepcopy(self.best_fit.dna)
        self.current_fit.draw_dna()

    def set_background_color(self):
        scc = SimpleColorChooser(self.best_fit_window)
        color = scc.choose_color()
        self.best_fit.background = color
        self.current_fit.background = color
        self.best_fit_window.color_value.configure(text=color)
        self.best_fit_window.color_sample.configure(background=color)

    def reset(self):
        '''restarts the image fitting with a new set of polygons'''
        self.running = False
        if tkMessageBox.askokcancel("",
                "New starting set of polygons?\nNote: you will lose all changes done so far."):
            self.best_fit.dna.init_dna()
            self.best_fit.mutations = 0
            self.best_fit.draw_dna()
            self.current_fit.dna.genes = copy.deepcopy(self.best_fit.dna.genes)
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
