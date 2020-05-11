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
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog, filedialog

import core.globals as glob



class startup_dialog(simpledialog.Dialog):
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
        self.new = False

        #call parent function from tkinter
        super().__init__(glob.root, title="Load or create")
        

    def body(self, parent):
        """Body.

        Builds user interface
        
        Parameters
        ----------
            parent: dialog root
        """
        #configure database folder
        self._lbl_folder = Label(parent, relief=GROOVE, width=60, text="Please select or create a database")
        self._lbl_folder.pack(expand=1, fill=BOTH, pady=5)
        

    def buttonbox(self):
        """Buttonbox.

        Build the standard button box for dialog. This just overrides the tkinter
        function to give access to the buttons for setting state
        """
        box = Frame(self)

        self.btn_ok = Button(box, text="New Database", width=20, command=self.ok, default=ACTIVE)
        self.btn_ok.pack(side=LEFT, padx=5, pady=5)

        self.btn_cancel = Button(box, text="Load Database", width=20, command=self.cancel)
        self.btn_cancel.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

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
        self.new = True
        super().ok()

    def apply(self):
        """apply.

        Store selected data in selection.
        """
        pass