'''
State engine widget.

The StateEngine class implements three buttons setting the state of an
animation.

The animation class must implement the following methods:
start()
run()
step()
pause()
reset()

'''

import Tkinter as tk

DEBUG = False

class StateEngine(object):
    """GUI state engine for animated simulations that can be started,
       paused and resumed, or reset from the beginning."""

    def __init__(self, parent, parent_window=None):
        ''' initializes a display with three buttons.  One must pass a
            reference to a "parent" which, itself, must have a reference to
            an animation "controls" with five methods: start, run, step, pause, reset.
        '''

        self.parent = parent
        if parent_window is None:   # for poly_image.py
            self.parent_window = self.parent
        else:
            self.parent_window = parent_window
        fnt = ("Arial", 12, "bold")

        ctrlFrame = tk.Frame(self.parent_window)
        self.start_btn = tk.Button(ctrlFrame, width=11, text="Start", font=fnt,
                                state = tk.NORMAL, padx=15, command=self.start)
        self.step_btn = tk.Button(ctrlFrame, width=11, text="Step", font=fnt,
                                state = tk.DISABLED, padx=15, command=self.step)
        self.reset_btn = tk.Button(ctrlFrame, width=11, text="Reset", font=fnt,
                                state = tk.DISABLED, padx=15, command=self.reset)
        for widget in self.start_btn, self.step_btn, self.reset_btn:
            widget.pack(side=tk.LEFT)
        ctrlFrame.pack(side=tk.TOP)
        self.set_state("START")

    def set_state(self, state):
        '''set the state'''
        self.state = state
        if DEBUG:
            print "setting state to: ", state
        if state == "START":
            self.start_btn.configure(text="Start", state=tk.NORMAL)
            self.step_btn.configure(state=tk.NORMAL)
            self.reset_btn.configure(state=tk.DISABLED)
        elif state == "RUNNING":
            self.start_btn.configure(text="Pause", state=tk.NORMAL)
            self.step_btn.configure(state=tk.DISABLED)
            self.reset_btn.configure(state=tk.DISABLED)
        elif state == "PAUSE":
            self.start_btn.configure(text="Resume", state=tk.NORMAL)
            self.step_btn.configure(state=tk.NORMAL)
            self.reset_btn.configure(state=tk.NORMAL)
        elif state == "DONE":
            self.start_btn.configure(text="Start", state=tk.DISABLED)
            self.step_btn.configure(state=tk.DISABLED)
            self.reset_btn.configure(state=tk.NORMAL)
        elif state == "TIMEOUT":
            self.start_btn.configure(state=tk.DISABLED)
            self.step_btn.configure(state=tk.DISABLED)
            self.reset_btn.configure(state=tk.DISABLED)
        else:
            raise NotImplementedError  # should never happen!

    def reset(self):
        '''resets the animation and the display'''
        self.parent.controls.reset()
        self.set_state("START")

    def step(self):
        '''steps through the animation'''
        self.set_state("TIMEOUT")
        if self.parent.controls.step():
            self.set_state("DONE")
        else:
            self.set_state("PAUSE")

    def start(self):
        '''start the animation'''
        if self.state in ["START", "PAUSE"]:
            self.set_state("RUNNING")
            if self.parent.controls.run():
                self.set_state("DONE")
            else:
                self.set_state("PAUSE")
        elif self.state == "RUNNING":  # displays "pause" on start button
            self.set_state("TIMEOUT")
            self.parent.controls.pause()
        else:
            raise NotImplementedError  # should never happen!


if __name__  == "__main__":
    DEBUG = True
    class TestAnimation(tk.Canvas):
        def __init__(self, parent):
            # the following line of code is REQUIRED for all apps.
            parent.controls = self
            tk.Canvas.__init__(self, parent)
            width, height = 300, 100
            self.config(width=width, height=height)
            self.info = self.create_text(width/2, height/2)
            self.pack()
            self.reset()

        def reset(self):
            self._redraw('"reset" called.')
            self.running = False
            self.fake_animation = self._iterator()

        def run(self):
            self._redraw('"run" called.')
            self.running = True
            while self.running:
                done = self.step()
            return done

        def step(self):
            result = self.fake_animation.next()
            self._redraw('"step" called; iteration=%d'%result)
            if result != 333:
                return False
            else:
                self._redraw("Reached the end of the simulation.")
                self.running = False
                return True

        def pause(self):
            self._redraw('"pause" called.')
            self.running = False

        def _iterator(self):
            i = 0
            while True:
                i += 1
                yield i

        def _redraw(self, text):
            self.itemconfig(self.info, text=text, fill="black",
                            font=("Arial", 14))
            self.update()

    main_app = tk.Tk()
    main_app.title('State Engine test')
    test_animation = TestAnimation(main_app)
    state_engine = StateEngine(main_app)
    main_app.mainloop()
