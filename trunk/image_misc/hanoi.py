"""  This has nothing to do with image fitting; it is just a fun application
adapted from code uploaded by Gregor Lindl on http://pygments.org/demo/250/
and is used to demonstrate the StateEngine class.
"""

import Tkinter as tk

from state_engine import StateEngine

class Disk(object):
    """Movable Rectangle on a Tkinter Canvas"""
    def __init__(self, cv, pos, length, height, colour):
        """creates disc on given Canvas cv at given position"""
        x0, y0 = pos
        x1, x2 = x0-length/2.0, x0+length/2.0
        y1, y2 = y0-height, y0
        self.cv = cv
        self.item = cv.create_rectangle(x1, y1, x2, y2,
                                        fill = "#%02x%02x%02x" % colour)
    def move_to(self, x, y, speed):
        """moves bottom center of disc to position (x,y).
           speed is intended to assume values from 1 to 10"""
        x1, y1, x2, y2 = self.cv.coords(self.item)
        x0, y0 = (x1 + x2)/2, y2
        dx, dy = x-x0, y-y0
        d = (dx**2 + dy**2)**0.5
        steps = int(d / (10*speed - 5)) + 1
        dx, dy = dx/steps, dy/steps
        for i in range(steps):
            self.cv.move(self.item, dx, dy)
            self.cv.update()
            self.cv.after(20)

class Tower(list):
    """Hanoi tower designed as a subclass of built-in type list"""
    def __init__(self, x, y, h):
        """ creates an empty tower.
            (x,y) is floor-level position of tower,
            h is height of the disks. """
        self.x = x
        self.y = y
        self.h = h
    def top(self):
        return self.x, self.y - len(self)*self.h

class Hanoi(object):
    """GUI for animated towers-of-Hanoi-game with upto 10 disks:"""
    def __init__(self, nb_disks, speed, parent):
        parent.controls = self
        self.init_hanoi_canvas(parent)
        self.init_hanoi_controls(parent, nb_disks, speed)
        self.new_game(nb_disks, speed)

    def init_hanoi_canvas(self, parent):
        """Creates canvas in which the towers and animated disks will be drawn."""
        self.cv = cv = tk.Canvas(parent, width=440, height=210)
        cv.pack()
        peg_1 = cv.create_rectangle( 75, 40,  85, 190, fill='darkgreen')
        peg_2 = cv.create_rectangle(215, 40, 225, 190, fill='darkgreen')
        peg_3 = cv.create_rectangle(355, 40, 365, 190, fill='darkgreen')
        floor = cv.create_rectangle( 5, 190, 435, 200, fill='black')

    def init_hanoi_controls(self, parent, nb_disks, speed):
        """Creates a frame for the speed and nb_disks controls."""
        fnt = ("Arial", 12, "bold")
        attrFrame = tk.Frame(parent)
        self.disks_label = tk.Label(attrFrame, width=7, text="disks:\n",
                                    font=fnt, height=2 )
        self.disks_slider = tk.Scale(attrFrame, from_=1, to_=10, orient=tk.HORIZONTAL,
                            font=fnt, length=75, showvalue=1,
                            repeatinterval=10, command=self.set_nb_of_disks)
        self.disks_slider.set(nb_disks)
        self.tempo_label = tk.Label(attrFrame, width=8, text="   speed:\n",
                                    font=fnt, height=2)
        self.tempo_slider = tk.Scale(attrFrame, from_=1, to_=10, orient=tk.HORIZONTAL,
                              font=fnt, length=100, showvalue=1,
                              repeatinterval=10, command=self.set_speed)
        self.tempo_slider.set(speed)
        self.move_count_label= tk.Label(attrFrame, width=5, padx=20,
                                        text=" move:\n0", anchor=tk.CENTER,
                                        font=fnt, height=2)
        for widget in (self.disks_label, self.disks_slider, self.tempo_label,
                        self.tempo_slider, self.move_count_label):
            widget.pack(side=tk.LEFT)
        attrFrame.pack(side=tk.TOP)

    def new_game(self, nb_disks, speed):
        """Sets Canvas to play on as well as default values for
        number of disks and animation-speed.
        move_count_display is a function with 1 parameter, which communicates
        the count of the actual move to the GUI containing the
        Hanoi-engine canvas."""
        self.nb_disks = nb_disks
        self.speed = speed
        self.running = False
        self.move_count = 0
        self.disks = []
        self.tower_1 = Tower( 80, 190, 15)
        self.tower_2 = Tower(220, 190, 15)
        self.tower_3 = Tower(360, 190, 15)
        self.reset()

    def set_nb_of_disks(self, e):
        '''sets the total number of disks used'''
        self.nb_disks = self.disks_slider.get()
        self.reset()

    def set_speed(self, e):
        '''sets the speed of the simulation'''
        self.speed = self.tempo_slider.get()

    def hanoi_solution(self, n, src, dest, temp):
        """The classical recursive Towers-Of-Hanoi algorithm."""
        if n > 0:
            for x in self.hanoi_solution(n-1, src, temp, dest):
                yield None
            yield self.move(src, dest)
            for x in self.hanoi_solution(n-1, temp, dest, src):
                yield None

    def move(self, src_tower, dest_tower):
        """moves uppermost disc of source tower to top of destination tower."""
        self.move_count += 1
        self.move_count_label.configure(text = "move: %d" % self.move_count)
        disc = src_tower.pop()
        x1, y1 = src_tower.top()
        x2, y2 = dest_tower.top()
        disc.move_to(x1, 20, self.speed)
        disc.move_to(x2, 20, self.speed)
        disc.move_to(x2, y2, self.speed)
        dest_tower.append(disc)

    def reset(self):
        """Setup of a [new] game."""
        self.disks_slider.configure(state=tk.NORMAL)
        self.disks_slider.configure(fg="black")
        self.disks_label.configure(fg="black")
        self.move_count = 0
        self.move_count_label.configure(text = "move: %d" % self.move_count)
        while self.tower_1:
            self.tower_1.pop()
        while self.tower_2:
            self.tower_2.pop()
        while self.tower_3:
            self.tower_3.pop()
        for s in self.disks:
            self.cv.delete(s.item)
        ## Fancy colouring of disks: red ===> blue
        if self.nb_disks > 1:
            colour_diff = 255 // (self.nb_disks-1)
        else:
            colour_diff = 0
        for i in range(self.nb_disks):  # setup tower_1
            length_diff = 100 // self.nb_disks
            length = 120 - i * length_diff
            s = Disk( self.cv, self.tower_1.top(), length, 13,
                         (255-i*colour_diff, 0, i*colour_diff))
            self.disks.append(s)
            self.tower_1.append(s)
        self.solution = self.hanoi_solution(self.nb_disks, self.tower_1,
                                            self.tower_3, self.tower_2)

    def run(self):
        """runs the Hanoi simulation"""
        self.running = True
        self.disks_slider.configure(state=tk.DISABLED)
        self.disks_slider.configure(fg="gray70")
        self.disks_label.configure(fg="gray70")
        try:
            while self.running:
                result = self.step()
            self.disks_slider.configure(state=tk.NORMAL)
            self.disks_slider.configure(fg="black")
            self.disks_label.configure(fg="black")
            return result  # True iff done
        except StopIteration:
            return True

    def step(self):
        '''single step - moving only one disk'''
        self.solution.next()
        return 2**self.nb_disks-1 == self.move_count

    def pause(self):
        """ ;-) """
        self.running = False

if __name__  == "__main__":
    main_app = tk.Tk()
    main_app.title('Towers of Hanoi')
    Hanoi(4, 5, main_app)
    StateEngine(main_app)
    main_app.mainloop()
