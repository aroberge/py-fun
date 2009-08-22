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
import Image, ImageTk, ImageStat # from PIL
import aggdraw

import src.dialogs as dialogs
from src.state_engine import StateEngine
from src.color_chooser import SimpleColorChooser
from src.fitness import FitnessRMS, FitnessMean

START_DEFAULT_COLOR = "#000000"

class DNA(object):
    '''A simple DNA class containing the required information for an
    image formed by a set of transparent polygons drawn on a background canvas
    '''
    def __init__(self, width, height, polygons=50, sides=6, background=(0, 0, 0)):
        self.polygons = polygons
        self.background = background
        self.sides = sides
        self.width = width
        self.height = height
        self.genes = []
        self.init_dna()

    def init_dna(self):
        self.genes = []
        for i in range(self.polygons):
            self.genes.append(self.create_random_polygon())

    def create_random_polygon(self):
        sides = []
        for i in range(self.sides):
            sides.append(randint(0, self.width))
            sides.append(randint(0, self.height))
        col = [randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)]
        return [sides, col]

    def mutate(self):
        selected = randint(0, self.polygons-1)
        _type = randint(0, 2)
        if _type == 0: # colour
            col_index = randint(0, 3)
            self.genes[selected][1][col_index] = randint(0, 255)
        elif _type == 1: # x coordinate
            coord = randint(0, self.sides-1)
            self.genes[selected][0][2*coord] = randint(0, self.width)
        elif _type == 2: # y coordinate
            coord = randint(0, self.sides-1)
            self.genes[selected][0][2*coord+1] = randint(0, self.height)

    def clone(self, other):
        self.background = other.background
        self.genes = copy.deepcopy(other.genes)
        self.polygons = other.polygons
        self.sides = other.sides
        self.width = other.width
        self.height = other.height

class AggDrawCanvas(tk.Canvas):
    """Drawing canvas that uses the Anti Grain Graphics (agg) library
    via aggdraw to draw polygon combinations.
    """
    def __init__(self, parent, polygons, sides):
        tk.Canvas.__init__(self, parent)
        self.parent = parent
        self.polygons = polygons
        self.sides = sides
        self.image_id = None
        self.img = None
        self.display_every = 1
        self.background = START_DEFAULT_COLOR
        # the following are used to calculate the average nb of mutation/second
        self.keep_last_n = 20
        self.gen_times = [1. for i in range(self.keep_last_n)]
        self.last_time = time.time()
        # finally, we display a placeholder image with default values
        self.set_size(200, 200)
        img = Image.new("RGBA", self.size_, START_DEFAULT_COLOR)
        s = aggdraw.Draw(img).tostring()
        raw = Image.fromstring('RGBA', self.size_, s)
        self.draw_on_screen(raw)
        self.pack(pady=2)

    def new_original(self, original):
        '''resets some basic values based on loading a new original image
           displayed elsewhere.
        '''
        self._fitness = FitnessRMS(draw=aggdraw.Draw)
        self.original = original
        self.mutations = 0
        _img = ImageTk.PhotoImage(self.original)
        self.set_size(_img.width(), _img.height())
        self.img = Image.new("RGBA", self.size_, self.background)
        self.dna = DNA(self.width_, self.height_, polygons=self.polygons,
                       sides=self.sides, background=self.background)
        self.context = aggdraw.Draw(self.img)

    def new_dna(self):
        self.dna = DNA(self.width_, self.height_, polygons=self.polygons,
                       sides=self.sides, background=self.background)

    def set_size(self, width, height):
        '''(re)sets the size parameters'''
        self.width_ = width
        self.height_ = height
        self.size_ = width, height
        self.config(width=width+2, height=height+2)

    def draw_dna(self):
        '''draws a series of polygons (dna) onto the aggdraw canvas'''
        brush = aggdraw.Brush(self.background, opacity=255)
        self.context.rectangle((0, 0, self.width_, self.height_), brush)
        if self.dna is not None:
            for gene in self.dna.genes:
                brush = aggdraw.Brush(tuple(gene[1][0:3]), opacity=gene[1][3])
                self.context.polygon(gene[0], brush)
        self.redraw()

    def redraw(self):
        '''actually redraw the new image and, when appropriate, updates
        the screen representation'''
        self.mutations += 1
        self.calc_average_time()
        s = self.context.tostring()
        raw = Image.fromstring('RGBA', self.size_, s)
        self.fitness = self._fitness.evaluate(self.original, raw, self.background)
        self.parent.update_info()
        if self.mutations % self.display_every:
            return
        else:
            self.draw_on_screen(raw)

    def draw_on_screen(self, raw_image):
        '''draws the image on the screen'''
        self.image = ImageTk.PhotoImage(raw_image)
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
        "Use the main window to end this program.")


class CurrentFitWindow(tk.Toplevel):
    def __init__(self, parent, title):
        tk.Toplevel.__init__(self)
        self.title(title)
        self.parent = parent
        main_frame = tk.Frame(self)
        # image frame
        self.image_frame = tk.Frame(main_frame)
        self.image_frame.update_info = self.update_info
        self.canvas = AggDrawCanvas(self.image_frame, polygons=50, sides=3)
        self.canvas.pack()
        self.protocol("WM_DELETE_WINDOW", prevent_accidental_closure)
        info_frame = tk.Frame(self.image_frame)
        info_frame.pack()
        self.info = tk.Label(info_frame, text="Current fitness")
        self.info.pack()
        self.show_every_btn = tk.Button(info_frame, width=25, height=1,
                    text="Display every %d image." % self.canvas.display_every,
                                         command=self.set_show_every)
        self.show_every_btn.pack()
        self.image_frame.pack(side=tk.RIGHT)
        main_frame.pack()

    def update_info(self):
        if self.canvas.ave_gen_per_second > 2:
            self.info.config(text = "Fitness: %2.2f\nMutations: %d\n[per second: %d]" %
                         (self.canvas.fitness, self.canvas.mutations,
                          int(self.canvas.ave_gen_per_second)))
        else:
            self.info.config(text = "Fitness: %2.2f\nMutations: %d\n[per second: %1.2f]" %
                         (self.canvas.fitness, self.canvas.mutations,
                          self.canvas.ave_gen_per_second))

    def set_show_every(self):
        set_frequency_dialog = dialogs.ImageFrequency(self)
        if set_frequency_dialog.result is not None:
            self.canvas.display_every = set_frequency_dialog.result
            self.show_every_btn.config(text =
                            "Display every %d image.\n" % self.canvas.display_every)


class OriginalImageWindow(tk.Toplevel):
    '''Class to display an original image, in any format
       supported by PIL'''
    def __init__(self, title):
        '''initializes the window containing the canvas on which the image
           is to be drawn'''
        tk.Toplevel.__init__(self)
        self.title(title)
        self.image_canvas = tk.Canvas(self)
        self.image_canvas.pack(side=tk.TOP, pady=2)
        self.protocol("WM_DELETE_WINDOW", prevent_accidental_closure)
        info_frame = tk.Frame(self)
        info_frame.pack()
        self.info_filename = tk.Label(info_frame, text="No image file loaded.")
        self.info_filename.pack()
        self.info_rgb = tk.Label(info_frame, text="")
        self.info_rgb.pack()
        #self.pack()


    def new_image(self, img, filename):
        '''displays a new image object onto a canvas, resizing the window
           as appropriate'''
        image = ImageTk.PhotoImage(img)
        width, height = image.width(), image.height()
        self.image_canvas.config(width=width, height=height)
        self.image_canvas.create_image(width/2, height/2, image=image)
        self.__image = image # need to keep a reference otherwise it disappears!
        stats = ImageStat.Stat(img)
        self.info_filename.config(text=filename)
        self.info_rgb.config(text="Median RGB: %s"%str(stats.median))

class App(object):
    """The main application window"""
    def __init__(self, parent):
        # required link to StateEngine:
        parent.controls = self
        parent.geometry("+400+40")
        self.parent = parent
        # Default parameters
        self.background = START_DEFAULT_COLOR
        self.polygons = 50
        self.sides = 6
        # Main window
        self.main_frame = tk.Frame(parent)
        self.main_frame.pack(side=tk.TOP)
        self.setup_controls()
        self.create_canvas()
        #
        self.original_image_window = OriginalImageWindow("Original image")
        self.original_image_window.geometry("+100+50")

        self.current_fit_window = CurrentFitWindow(self, "Current fit")
        self.current_fit_window.geometry("+100+400")
        #
        self.current_fit = self.current_fit_window.canvas

    def setup_controls(self):
        left_frame = tk.Frame(self.main_frame)
        left_frame.pack(side=tk.LEFT)
        filename_button = tk.Button(left_frame, text="New image",
                                    command=self.load_image)
        filename_button.pack(side=tk.TOP)
        # color setting
        set_color_btn = tk.Button(left_frame, text="Select background color",
                                        command=self.set_background_color)
        set_color_btn.pack()
        small_frame = tk.Frame(left_frame)
        self.color_value = tk.Label(small_frame)
        self.color_value.configure(text=self.background, width=10)
        self.color_value.pack(side=tk.LEFT)
        self.color_sample = tk.Label(small_frame)
        self.color_sample.configure(width=10)
        self.color_sample.pack(side=tk.LEFT)
        small_frame.pack()
        self.color_sample.configure(background=self.background)
        # dna save/load
        small_frame = tk.Frame(left_frame)
        save_polygons_btn = tk.Button(small_frame, text="Save dna",
                                        command=self.save_poly)
        save_polygons_btn.pack(side=tk.LEFT)
        load_polygons_btn = tk.Button(small_frame, text="Load dna",
                                        command=self.load_poly)
        load_polygons_btn.pack(side=tk.LEFT)
        small_frame.pack()
        # polygon parameters
        self.set_nb_polygons_btn = tk.Button(left_frame,
                                             text="%d polygons" % self.polygons,
                                             command=self.set_nb_polygons)
        self.set_nb_polygons_btn.pack(side=tk.TOP)
        self.set_nb_sides_btn = tk.Button(left_frame,
                                        text="%d sides per polygon" % self.sides,
                                        command=self.set_nb_sides)
        self.set_nb_sides_btn.pack()
        # image saving
        self.save_png_btn = tk.Button(left_frame, text="Save png",
                                      command=self.save_image)
        self.save_png_btn.pack(side=tk.LEFT)
        self.save_svg_btn = tk.Button(left_frame, text="Save svg",
                                      command=self.save_image)
        self.save_svg_btn.pack(side=tk.LEFT)

    def create_canvas(self):
        '''creates the canvas used to hold the best fit image'''
        self.main_frame.update_info = self.update_info
        self.best_fit = AggDrawCanvas(self.main_frame, self.polygons, self.sides)
        self.best_fit.pack()
        self.add_info()

    def add_info(self):
        info_frame = tk.Frame(self.main_frame)
        info_frame.pack()
        self.display_every = 1
        self.info = tk.Label(info_frame, text="Current fitness")
        self.info.pack()
        self.show_every_btn = tk.Button(info_frame, height=1,
                    text="Display every %d image." % self.display_every,
                                         command=self.set_show_every)
        self.show_every_btn.pack()

    def set_show_every(self):
        set_frequency_dialog = dialogs.ImageFrequency(self.parent)
        if set_frequency_dialog.result is not None:
            self.best_fit.display_every = set_frequency_dialog.result
            self.show_every_btn.config(text =
                            "Display every %d image.\n" % self.best_fit.display_every)

    def load_image(self):
        filename = tkFileDialog.askopenfilename()
        if not filename:
            return
        try:
            self.original = Image.open(filename)
        except IOError:
            print "ignored IOError; most likely not a valid image file."
            return
        self.original_image_window.new_image(self.original, filename)
        self.best_fit.new_original(self.original)
        self.best_fit.draw_dna()
        self.current_fit.new_original(self.original)
        self.current_fit.dna.clone(self.best_fit.dna)
        self.current_fit.draw_dna()

    def save_image(self):
        dialogs.SaveImage()

    def set_nb_polygons(self):
        polygons_dialog = dialogs.NumberOfPolygons(self.parent)
        try:
            self.polygons = int(polygons_dialog.result)
            self.set_nb_polygons_btn.config(text="%d polygons" % self.polygons)
            self.best_fit.polygons = self.polygons
            self.best_fit.dna.polygons = self.polygons
            self.new_dna()
        except:
            print "could not set nb_polygons."

    def set_nb_sides(self):
        sides_dialog = dialogs.NumberOfSides(self.parent)
        try:
            self.sides = int(sides_dialog.result)
            self.set_nb_sides_btn.config(text="%d sides per polygon" % self.sides)
            self.best_fit.sides = self.sides
            self.current_fit.sides = self.sides
            self.new_dna()
        except:
            print "could not set nb_sides."

    def save_poly(self):
        filename = tkFileDialog.asksaveasfilename()
        if not filename:
            return
        filehandle = open(filename, "w")
        dna = []
        dna.append(self.best_fit.background)
        dna.append(str(self.best_fit.dna.polygons))
        dna.append(str(self.best_fit.dna.sides))
        coords = range(2*self.best_fit.dna.sides)
        for gene in self.best_fit.dna.genes:
            for item in gene:
                for value in item:
                    dna.append(str(value))
        filehandle.write(' '.join(dna))

    def load_poly(self):
        filename = tkFileDialog.askopenfilename()
        if not filename:
            return
        items = open(filename).read().split()
        self.best_fit.background = items[0]
        self.best_fit.dna.polygons = int(items[1])
        self.best_fit.dna.sides = int(items[2])
        nb_coords = 2*self.best_fit.dna.sides
        nb_subitems = nb_coords + 4  # 4 color values per polygon
        offset = 3  # first 3 values are excluded
        self.best_fit.dna.genes = []
        for i in range(self.best_fit.dna.polygons):
            coords = []
            color = []
            for j in range(nb_coords):
                coords.append(int(items[offset+i*nb_subitems + j]))
            for j in range(4):
                color.append(int(items[offset+i*nb_subitems + nb_coords + j]))
            self.best_fit.dna.genes.append([coords, color])
        self.current_fit.background = self.best_fit.background
        self.current_fit.dna.polygons = self.best_fit.dna.polygons
        self.current_fit.dna.sides = self.best_fit.dna.sides
        self.current_fit.dna = copy.deepcopy(self.best_fit.dna)

    def update_info(self):
        if self.best_fit.ave_gen_per_second > 2:
            self.info.config(text = "Fitness: %2.2f\nMutations: %d\n[per second: %d]" %
                         (self.best_fit.fitness, self.best_fit.mutations,
                          int(self.best_fit.ave_gen_per_second)))
        else:
            self.info.config(text = "Fitness: %2.2f\nMutations: %d\n[per second: %1.2f]" %
                         (self.best_fit.fitness, self.best_fit.mutations,
                          self.best_fit.ave_gen_per_second))

    def set_background_color(self):
        scc = SimpleColorChooser(self.parent)
        color = scc.choose_color()
        self.best_fit.background = color
        self.current_fit.background = color
        self.color_value.configure(text=color)
        self.color_sample.configure(background=color)

    def new_dna(self):
        self.best_fit.new_dna()
        self.best_fit.dna.init_dna()
        self.best_fit.mutations = 0
        self.best_fit.draw_dna()
        self.current_fit.new_dna()
        self.current_fit.dna.clone(self.best_fit.dna)
        self.current_fit.mutations = 0
        self.current_fit.draw_dna()

    def reset(self):
        '''restarts the image fitting with a new set of polygons'''
        self.running = False
        # the following try/except block is used when the start button
        # has been called before an image has been loaded and the user
        # then needs to press "reset".
        try:
            if self.best_fit.dna is None:
                return
        except:
            return
        if tkMessageBox.askokcancel("",
                "New starting set of polygons?\n"
                "Note: you will lose all changes done so far."):
            self.new_dna()

    def run(self):
        '''starts or resume/restarts the "fitting".'''
        try:
            if self.best_fit.dna is None:
                self.new_dna()
        except:
            tkMessageBox.showinfo("", "You have to load an image first.")
            return True
        self.running = True
        while self.running:
            done = self.step()
        return done

    def step(self):
        '''single mutation step; currently never ends on its own'''
        try:
            if self.best_fit.dna is None:
                pass
        except:
            tkMessageBox.showinfo("", "You have to load an image first.")
            return True
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
    StateEngine(main_app)
    main_app.mainloop()
