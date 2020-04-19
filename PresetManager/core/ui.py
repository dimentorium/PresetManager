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
from reaper.preset import save
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog, filedialog

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



def save_preset_dialog(parent):
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
    save_dialog = SavePreset(parent)
    cancelled = save_dialog.cancelled
    result = save_dialog.selection
    return cancelled, result

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

    def __init__(self, parent):
        """Init.

        Initialize class properties.
        
        Parameters
        ----------
            parent: parent frame calling dialog
        """
        self.selection = None
        self.cancelled = False
        super().__init__(parent, title="Save Preset")

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

        #add frame for checkboxes
        self._frame = Frame(parent, relief=GROOVE)
        self._frame.pack(expand=1, fill=BOTH)

        #create checkboxes for tags. List is just for demo purposes
        self.tags = ["string","brass","synth"]
        self.checkboxes = []
        for tag in self.tags:
            #create a var that is later used for getting status of checboxes
            checked = IntVar()
            cb = Checkbutton(self._frame, text=tag, variable=checked)
            cb.pack(padx=1, pady=2, anchor=W)
            self.checkboxes.append(checked)


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
        result_list = []
        #check which tags are selected an store them with presetname
        for tag, box in zip(self.tags,self.checkboxes) :
            if box.get():
                result_list.append(tag)
        self.selection = [self._entry.get(), result_list]