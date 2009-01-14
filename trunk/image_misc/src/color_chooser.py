# adapted from
# http://www-ihm.lri.fr/~roussel/enseignement/PYTK/exercises/colorchooser/index.html

import Tkinter as tk

class SimpleColorChooser(object):

    def __init__(self, master):
        self.master = master
        self.top = None

    def choose_color(self):
        self.setup_widgets()
        self.top.grab_set()
        self.top.wait_window(self.top)
        self.top = None
        return self.color

    def setup_widgets(self):
        self.top = tk.Toplevel(self.master)
        self.top.title("Color chooser")
        self.top.selection_handle(self.selection_request)

        left = tk.Frame(self.top)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=2, pady=2)

        self.red = tk.Scale(left, label="Red", from_=0, to=255, length=256,
                            orient=tk.HORIZONTAL, command=self.update_color)
        self.red.pack(fill=tk.X, expand=1)
        self.green = tk.Scale(left, label="Green", from_=0, to=255, length=256,
                            orient=tk.HORIZONTAL, command=self.update_color)
        self.green.pack(fill=tk.X, expand=1)
        self.blue = tk.Scale(left, label="Blue", from_=0, to=255, length=256,
                            orient=tk.HORIZONTAL, command=self.update_color)
        self.blue.pack(fill=tk.X, expand=1)

        right = tk.Frame(self.top)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=2, pady=2)

        self.value = tk.Label(right)
        self.value.pack(fill=tk.X, padx=2, pady=2)
        self.sample = tk.Label(right)
        self.sample.pack(fill=tk.BOTH, expand=1, padx=2, pady=2)
        self.sample.config(width=10)
        copy = tk.Button(right, text="Ok", command=self.copy_color_value)
        copy.pack(fill=tk.X, padx=2, pady=2)

    def update_color(self, *args):
        if not self.top: return
        self.color = "#%02x%02x%02x"%(self.red.get(), self.green.get(), self.blue.get())
        self.value.configure(text=self.color)
        self.sample.configure(background=self.color)

    def copy_color_value(self):
        self.top.selection_own()
        self.top.destroy()

    def selection_request(self, offset, length):
        return self.color

if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.wm_withdraw()

    scc = SimpleColorChooser(main_window)
    print scc.choose_color()
