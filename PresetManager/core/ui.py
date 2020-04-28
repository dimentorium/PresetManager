# -*- coding: utf-8 -*-
"""UI module.

Contains classes for UI elements and dialogs that can be used

Classes:
    Choice Dialog: Dialog for selecting an item from a list
    SavePreset Dialog: Dialog for saving and configuring a preset

Functions

Todo:
    * Refactoring to hve cleaner structure

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""
from core.globals import root
from reaper.preset import save
import reaper.render as render
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog, filedialog

import core.items as items
import core.globals as glob

def new_database_dialog():
    """Save Preset Dialog.

    Wrapper function showing dialog and returning data

    Parameters
    ----------
        parent: root frame calling dialog
        
    Returns:
    -------
        cancelled: True if dialog was cancelled false if dialog is OK
        result: list with preset name and list of tags
    """
    #call dialog and read out returning values
    database_dialog = NewDatabase()
    cancelled = database_dialog.cancelled
    name = database_dialog.database_name
    folder = database_dialog.database_folder
    return cancelled, name, folder

class NewDatabase(simpledialog.Dialog):
    """NewDatabase.

    Dialog for creating new database

    Methods
    -------
        init: init class and set properties
        body: build user interface
        validate: check if input is ok
        apply: update return values

    Properties
    ----------
        cancelled: status of dialog
        database_folder: folder of current database
        database_name: name of database
    """

    def __init__(self):
        """Init.

        Initialize class properties.
        """
        #init properties
        self.cancelled = True
        self.database_folder = ""
        self.database_name = ""

        #call parent function from tkinter
        super().__init__(glob.root, title="Configure Database")

    def body(self, parent):
        """Body.

        Builds user interface
        
        Parameters
        ----------
            parent: dialog root
        """
        #configure database name
        self._var_name = StringVar()
        self._var_name.trace("w", self.update_ui)
        self._entry_name = Entry(parent, text="Please enter database name", textvariable=self._var_name)
        self._entry_name.pack(expand=1, fill=BOTH,pady=5)

        #configure database folder
        self._lbl_folder = Label(parent, relief=GROOVE)
        self._lbl_folder.pack(expand=1, fill=BOTH, pady=5)

        self.btn_folder = Button(parent,text="Select Folder", command=self.select_folder)
        self.btn_folder.pack(expand=1, fill=BOTH,pady=5)

    def buttonbox(self):
        """Buttonbox.

        Build the standard button box for dialog. This just overrides the tkinter
        function to give access to the buttons for setting state
        """
        box = Frame(self)

        self.btn_ok = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        self.btn_ok.pack(side=LEFT, padx=5, pady=5)
        self.btn_ok['state'] = DISABLED

        self.btn_cancel = Button(box, text="Cancel", width=10, command=self.cancel)
        self.btn_cancel.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def update_ui(self, *args):
        """Update UI.

        Update status of control elements according to selection
        
        Parameters
        ----------
            args: evt arguments set by the tkinter framework
        """
        #update state of OK button according to preset name
        if self._lbl_folder['text'] != "" and self._var_name.get() != "":
            self.btn_ok['state'] = NORMAL
        else:
            self.btn_ok['state'] = DISABLED

    def select_folder(self):
        """Select Folder.

        Open Dialog to select folder for database
        """
        self._lbl_folder['text'] = filedialog.askdirectory(title="Select folder")
        self.update_ui()

    def validate(self) -> int:
        """Validate.

        Function validating user data
            
        Returns:
        -------
            int: 1 for OK, 0 for not ok
        """
        return 1

    def ok(self):
        """OK.

        Function called when OK is pressed
        """
        self.cancelled = False
        super().ok()

    def apply(self):
        """apply.

        Store selected data in selection.
        """
        self.database_folder = self._lbl_folder['text']
        self.database_name = self._entry_name.get() + ".bin"

class ChoiceDialog(simpledialog.Dialog):
    """ChoiceDialog.

    Dialog for selecting an item from a list of possible choices.
    Class is derived from simpledialog.Dialog

    Methods
    -------
        init: init class and set properties
        body: build user interface
        validate: check if input is ok
        apply: update return values

    Properties
    ----------
        selection: selected item
        items: list of items from which can be selected
        text: title of dialog
        message: label to show text message
        tree: tree from which the item is selected
    """

    def __init__(self, parent, title: str, text: str, items: list):
        """Init.

        Initialize class properties.
        
        Parameters
        ----------
            parent: parent frame calling dialog
            title: title of dialog
            text: message for user
            items: list for selection
        """
        #init properties
        self.selection = None
        self._items = items
        self._text = text

        #call parent function from tkinter
        super().__init__(parent, title=title)

    def body(self, parent) -> Treeview:
        """Body.

        Builds user interface
        
        Parameters
        ----------
            parent: dialog root
            
        Returns:
        -------
            tree: tree for selection
        """
        #configure message label
        self._message = Label(parent, text=self._text)
        self._message.pack(expand=1, fill=BOTH, padx=5, pady=5)

        #configure treeview
        self._tree = Treeview(parent)
        self._tree.pack(expand=1, fill=BOTH, side=TOP, padx=5, pady=5)
        for item in self._items:
            self._tree.insert("", END, text=self._items[item].preset_name)
        return self._tree

    def validate(self) -> int:
        """Validate.

        Function validating user data
            
        Returns:
        -------
            int: 1 for OK, 0 for not ok
        """
        #if no item is selected, than result is not valid
        if len(self._tree.selection()) == 0:
            return 0
        return 1

    def apply(self):
        """apply.

        Store selected data in selection.
        """
        self.selection = self._tree.item(self._tree.focus())



def save_preset_dialog(preset: items.vstipreset):
    """Save Preset Dialog.

    Wrapper function showing dialog and returning data

    Parameters
    ----------
        parent: root frame calling dialog
        
    Returns:
    -------
        cancelled: True if dialog was cancelled false if dialog is OK
        result: list with preset name and list of tags
    """
    #call dialog and read out returning values
    save_dialog = SavePreset(preset)
    cancelled = save_dialog.cancelled
    return cancelled

class SavePreset(simpledialog.Dialog):
    """ChoiceDialog.

    Dialog for selecting an item from a list of possible choices.
    Class is derived from simpledialog.Dialog

    Methods
    -------
        init: init class and set properties
        body: build user interface
        update_ui: updates state of controls
        ok: function called when OK is pressed
        buttonbox: function generating the button box
        validate: check if input is ok
        apply: update return values

    Properties
    ----------
        selection: selected item
        cancelled: status of dialog
        entry_text: storing entry
        entry: control for entering preset name
        frame: frame for checkboxes
        tags: tags that are displayed to user
        checkboxes: list of all checkboxes
        btn_ok: button for OK
        btn_cancel: button for cancel
    """

    def __init__(self, preset: items.vstipreset):
        """Init.

        Initialize class properties.
        
        Parameters
        ----------
            parent: parent frame calling dialog
        """
        self.selection = None
        self.cancelled = False
        self.__preset = preset
        super().__init__(glob.root, title="Save Preset")

    def body(self, parent):
        """Body.

        Builds user interface
        
        Parameters
        ----------
            parent: dialog root
        """
        #configure entry field and link to variable
        self._entry_text = StringVar()
        self._entry_text.trace("w", self.update_ui)
        self._entry = Entry(parent, text="Please configure preset to save", textvariable=self._entry_text)
        self._entry.pack(expand=1, fill=BOTH,pady=5)

        #configure render checkbox
        self._entry_render = BooleanVar()
        self._cb_render = Checkbutton(parent,text="Render", variable=self._entry_render)
        self._cb_render.pack(padx=1, pady=2, anchor=W)

        #add frame for checkboxes
        self._frame = Frame(parent, relief=GROOVE, padding=5)
        self._frame.pack(expand=1, fill=BOTH)

        #create checkboxes for tags. List is just for demo purposes
        self.tags = glob.item_tags
        self.checkboxes = []
        row = 0
        column = 0
        for tag in self.tags:
            #create a var that is later used for getting status of checboxes
            checked = IntVar()
            cb = Checkbutton(self._frame, text=tag, variable=checked)
            cb.grid(row=row, column=column, sticky='ew')
            self.checkboxes.append(checked)
            column += 1
            if column >= 3:
                column = 0
                row += 1


    def update_ui(self, *args):
        """Update UI.

        Update status of control elements according to selection
        
        Parameters
        ----------
            args: evt arguments set by the tkinter framework
        """
        #update state of OK button according to preset name
        if self._entry_text.get() != "":
            self.btn_ok['state'] = NORMAL
        else:
            self.btn_ok['state'] = DISABLED


    def buttonbox(self):
        """Buttonbox.

        Build the standard button box for dialog. This just overrides the tkinter
        function to give access to the buttons for setting state
        """
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
        """OK.

        Function called when OK is pressed
        """
        self.cancelled = False
        super().ok()


    def validate(self):
        """Validate.

        Function called for validating data, currently only returning 1
        """
        return 1

    def apply(self):
        """Apply.

        Store selection in properties for usage
        """
        self.__preset.preset_name = self._entry.get()
        self.__preset.tags = []

        if self._entry_render.get():
            self.__preset.preview_path = self.render_preset()

        #check which tags are selected an store them with presetname
        for tag, box in zip(self.tags,self.checkboxes) :
            if box.get():
                self.__preset.tags.append(tag)

    def render_preset(self):
        path = glob.database_folder
        renderfilepath = render.render_audio(path, self._entry.get(), self.__preset.chunk)
        return renderfilepath
