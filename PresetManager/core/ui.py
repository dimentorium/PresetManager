from reaper.preset import save
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



def save_preset_dialog(parent):
    save_dialog = SavePreset(parent)
    cancelled = save_dialog.cancelled
    result = save_dialog.selection
    return cancelled, result

class SavePreset(simpledialog.Dialog):
    def __init__(self, parent):
        self.selection = None
        self.cancelled = False
        super().__init__(parent, title="Save Preset")

    def body(self, parent):
        self._entry_text = StringVar()
        self._entry_text.trace("w", self.update_ui)
        self._entry = Entry(parent, text="Please configure preset to save", textvariable=self._entry_text)
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


    def update_ui(self, *args):
        if self._entry_text.get() != "":
            self.btn_ok['state'] = NORMAL
        else:
            self.btn_ok['state'] = DISABLED


    def buttonbox(self):
        box = Frame(self)

        self.btn_ok = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        self.btn_ok.pack(side=LEFT, padx=5, pady=5)
        self.btn_ok['state'] = DISABLED

        self.btn_cancel = Button(box, text="Cancel", width=10, command=self.cancel)
        self.btn_cancel.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self):
        self.cancelled = False
        super().ok()


    def validate(self):
        return 1

    def apply(self):
        result_list = []
        for tag, box in zip(self.tags,self.checkboxes) :
            if box.get():
                result_list.append(tag)
        self.selection = [self._entry.get(), result_list]