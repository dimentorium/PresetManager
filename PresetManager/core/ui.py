from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog, filedialog

class ChoiceDialog(simpledialog.Dialog):
    def __init__(self, parent, title, text, items):
        self.selection = None
        self._items = items
        self._text = text
        super().__init__(parent, title=title)

    def body(self, parent):
        self._message = Label(parent, text=self._text)
        self._message.pack(expand=1, fill=BOTH, padx=5, pady=5)

        self._tree = Treeview(parent)
        self._tree.pack(expand=1, fill=BOTH, side=TOP, padx=5, pady=5)
        for item in self._items:
            self._tree.insert("", END, text=self._items[item].preset_name)
        return self._tree

    def validate(self):
        if len(self._tree.selection()) == 0:
            return 0
        return 1

    def apply(self):
        self.selection = self._tree.item(self._tree.focus())

class SavePreset(simpledialog.Dialog):
    def __init__(self, parent):
        self.selection = None
        super().__init__(parent, title="Save Preset")

    def body(self, parent):
        self._message = Label(parent, text="Please configure preset to save")
        self._message.pack(expand=1, fill=BOTH)

        self._entry = Entry(parent, text="Please configure preset to save")
        self._entry.pack(expand=1, fill=BOTH,pady=5)

        self._frame = Frame(parent, relief=GROOVE)
        self._frame.pack(expand=1, fill=BOTH)

        self.tags = ["string","brass","synth"]
        self.checkboxes = []
        for tag in self.tags:
            checked = IntVar()
            cb = Checkbutton(self._frame, text=tag, variable=checked)
            cb.pack(padx=1, pady=2, anchor=W)
            self.checkboxes.append(checked)

    def validate(self):
        return 1

    def apply(self):
        result_dict = {}
        for tag, box in zip(self.tags,self.checkboxes) :
            result_dict[tag] = box.get()
        self.selection = [self._entry.get(), result_dict]