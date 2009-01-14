'''Simple dialogs for the main application'''

import tkMessageBox, tkSimpleDialog
import Tkinter as tk

class NotImplementedDialog(object):
    def __init__(self, message):
        tkMessageBox.showinfo("", message)

class SaveImage(NotImplementedDialog):
    def __init__(self):
        NotImplementedDialog.__init__(self, "Saving image not yet implemented")

class ValidatedIntegerDialog(tkSimpleDialog.Dialog):
    def validate(self):
        result = self.choice.get()
        if result == '':
            return
        try:
            self.result = int(result)
            if self.result < self.min_value:
                raise
        except:
            tkMessageBox.showerror('',
                        "Integer value greater than %s required."%self.min_value)
            self.result = None
        return self.result

class ImageFrequency(ValidatedIntegerDialog):
    def body(self, parent):
        tk.Label(parent, text="Select the image drawing frequency").pack()
        self.choice = tk.Entry(parent)
        self.choice.pack()
        self.min_value = 1
        return self.choice # initial focus

class NumberOfPolygons(ValidatedIntegerDialog):
    def body(self, parent):
        tk.Label(parent, text="Select the number of polygons").pack()
        self.choice = tk.Entry(parent)
        self.choice.pack()
        self.min_value = 1
        return self.choice # initial focus

class NumberOfSides(ValidatedIntegerDialog):
    def body(self, parent):
        tk.Label(parent, text="Select the number of sides per polygon").pack()
        self.choice = tk.Entry(parent)
        self.choice.pack()
        self.min_value = 3
        return self.choice # initial focus