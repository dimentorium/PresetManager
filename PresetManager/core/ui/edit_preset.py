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
import os.path as path
import reaper.render as render
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog, filedialog

import core.items as items
import core.globals as glob
from core import tags, item_list, actions


class Edit_Preset(simpledialog.Dialog):
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
        self.cancelled = True
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
        entry_label = Label(parent, text="Preset Name")
        entry_label.grid(row=0, column=0, padx=5, pady=1, sticky='ew')
        self._entry_text = StringVar()
        self._entry_text.set(self.__preset.preset_name)
        self._entry_text.trace("w", self.update_ui)
        self._entry = Entry(parent, textvariable=self._entry_text)
        self._entry.grid(row=0, column=1, columnspan=2, padx=5, pady=1, sticky='ew')
        self._entry.focus()

        #configure rating field
        rate_label = Label(parent, text="Rating")
        rate_label.grid(row=1, column=0, padx=5, pady=1, sticky='ew')
        self._rating_value = IntVar()
        self._rating_value.set(self.__preset.rating)
        self._rating = Spinbox(parent, values=(1, 2, 3, 4, 5), textvariable=self._rating_value)
        self._rating.grid(row=1, column=1, columnspan=2, padx=5, pady=1, sticky='ew')

        #configure favorite checkbox
        favorite_label = Label(parent, text="Favorite")
        favorite_label.grid(row=2, column=0, padx=5, pady=1, sticky='ew')
        self._entry_favorite = BooleanVar()
        self._entry_favorite.set(self.__preset.favorite)
        self._cb_favorite = Checkbutton(parent, variable=self._entry_favorite)
        self._cb_favorite.grid(row=2, column=1, padx=5, pady=1, sticky='ew')

        #configure render checkbox
        preview_label = Label(parent, text="Preview")
        preview_label.grid(row=3, column=0, padx=5, pady=1, sticky='ew')
        self._entry_preview = BooleanVar()
        if path.exists(self.__preset.preview_path):
            self._entry_preview.set(True)
        self._cb_preview = Checkbutton(parent, variable=self._entry_preview)
        self._cb_preview.grid(row=3, column=1, padx=5, pady=1, sticky='ew')
        preview_explanation_label = Label(parent, text="Generates Preview")
        preview_explanation_label.grid(row=3, column=2, padx=5, pady=1, sticky='ew')

        Separator(parent, orient="horizontal").grid(row=4, columnspan=3, padx=5, pady=5, sticky='ew')

        #custom tags label
        tags_label = Label(parent, text="Tags")
        tags_label.grid(row=5, column=0, padx=5, pady=1, sticky='ew')
        self._entry_custom_tags = StringVar()
        self._custom_tags = Entry(parent, textvariable=self._entry_custom_tags)
        self._custom_tags.grid(row=5, column=1, columnspan=2, padx=5, pady=1, sticky='ew')

        #add frame for checkboxes
        self._frame = ScrollableFrame(parent, relief=GROOVE, padding=5)
        self._frame.grid(row=6, columnspan=3, padx=5, pady=1, sticky='ew')

        #create checkboxes for tags. List is just for demo purposes
        self.tags = tags.get()
        self.checkboxes = []
        row = 0
        column = 0
        for tag in self.tags:
            #create a var that is later used for getting status of checboxes
            checked = IntVar()
            if tag in self.__preset.tags:
                checked.set(True)
            cb = Checkbutton(self._frame.scrollable_frame, text=tag, variable=checked)
            cb.grid(row=row, column=column, sticky='ew')
            #cb.pack()
            self.checkboxes.append(checked)
            column += 1
            if column >= 2:
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
        self.update_ui()

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
        self.__preset.rating = self._rating_value.get()
        self.__preset.favorite = self._entry_favorite.get()

        #generate preview if not yet existing
        if self._entry_preview.get():
            if not path.exists(self.__preset.preview_path):
                self.__preset.preview_path = self.render_preset()

        #check which tags are selected and store them with presetname
        self.__preset.tags = []
        for tag, box in zip(self.tags,self.checkboxes):
            if box.get():
                self.__preset.tags.append(tag)

        #append custom tags from entery field
        custom_tag_string = self._entry_custom_tags.get()
        if custom_tag_string != "":
            custom_tag_list = [x.strip() for x in custom_tag_string.split(',')]
            self.__preset.tags.extend(custom_tag_list)

    def render_preset(self):
        """Renders preset currently edited

        Returns:
            renderfilepath[str] -- path to preview file
        """
        renderfilepath = render.render_audio(item_list.folder_name(), self._entry.get(), self.__preset.chunk)
        return renderfilepath


class ScrollableFrame(Frame):
    """Scrollable frame widget

    Arguments:
        Frame {Frame} -- Base class from TKinter
    """
    def __init__(self, container, *args, **kwargs):
        """Initialize scrollable frame widget

        Arguments:
            container {unknown} -- parent widget where frame is placed in
        """
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
