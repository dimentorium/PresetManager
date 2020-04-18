# -*- coding: utf-8 -*-
"""CPreset Manager Main.

Main startup to run the Prese Manager

Classes:
    controller: main classes handling the program and dataflow

Functions

Todo:
    * Refactoring to hve cleaner structure

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""

#======================== Imorts Section ====================#
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog, filedialog

import textwrap

import pickle

import reaper.preset as rp
import reapy
import core.ui as ui
import core.items as items
#============================================================#

class main_view():
    """Main View Class.

    Main Windows built with ttk and all controller functions

    Methods
    -------
        init: init class and create window
        search: get search string
        save_preset: save a preset from a Reaper track
        load_preset: load a preset to a Reaper track
        load_database: load database from file
        save_database: save database to file
        new_database: create empty database
        select_item: event when item in preset tree is selected
        update_info: update info tree
        update_list: update preset tree
        update_ui: update UI element status

    Properties
    ----------
        preset_list: list of all presets, database
        _search_filter: string that is used for searching
        _selected_item: item selected in preset tree
        root: root windo for all elements
        btn_new_database: button to create new database
        btn_load_database: button for loading database
        btn_save_database: button for saving database
        btn_load_preset: button for loading preset
        btn_save_preset: button for saving preset
        _entry_text: variable for search string
        search_box: entry field for search string
        presettree: tree for displaying database
        presetinfo: tree for displaying selected item information
    """
    
    def __init__(self):
        """Init.

        Initialize class properties.
        Builds window and links function calls
        """
        self.preset_list = {}
        self._search_filter = ""
        self._selected_item = None
        self.root = Tk()
        self.root.title("Reaper Preset Manager")
        
        current_row = 0

        #Buttons for handling database
        self.btn_new_database = Button(self.root,text="New Database", command=self.new_database)
        self.btn_new_database.grid(row=current_row,column=0, padx=5, pady=5, sticky='ew')

        self.btn_load_database = Button(self.root,text="Load Database", command=self.load_database)
        self.btn_load_database.grid(row=current_row,column=1, padx=5, pady=5, sticky='ew')

        self.btn_save_database = Button(self.root,text="Save Database", command=self.save_database)
        self.btn_save_database.grid(row=current_row,column=2, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Separator
        Separator(self.root,orient="horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Buttons for handling presets
        self.btn_load_preset = Button(self.root,text="Load Preset", command=self.load_preset)
        self.btn_load_preset.grid(row=current_row,column=0, padx=5, pady=5, sticky='ew')
        
        self.btn_save_preset = Button(self.root,text="Save Preset", command=self.save_preset)
        self.btn_save_preset.grid(row=current_row,column=1, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Separator
        Separator(self.root,orient="horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Search Field
        Label(self.root,text="Search").grid(row=current_row, padx=5, column=0, sticky='w')
        
        self._entry_text = StringVar()
        self._entry_text.trace("w", self.search)
        self.search_box = Entry(self.root, textvariable=self._entry_text)
        self.search_box.grid(row=current_row, column=1,columnspan=3, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Separator
        Separator(self.root,orient="horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Treeview for presets
        self.presettree = Treeview(self.root)
        self.presettree.grid(row=current_row, rowspan=8, columnspan=3, padx=5, pady=5, sticky='ew')
        self.presettree.bind("<<TreeviewSelect>>", self.select_item)
        self.presettree["columns"] = ("Plugin")
        self.presettree.heading("#0", text="Preset")
        self.presettree.heading("Plugin", text="Plugin")
        vsb = Scrollbar(self.root, orient="vertical", command=self.presettree.yview)
        vsb.grid(row=current_row, rowspan=8, column=3, pady=5,sticky='nsw')
        self.presettree.configure(yscrollcommand=vsb.set)
        current_row +=8

        #Treeview for presets
        self.presetinfo = Treeview(self.root)
        self.presetinfo.grid(row=current_row, rowspan=2, columnspan=3, padx=5, pady=5, sticky='ew')
        self.presetinfo["columns"] = ("Value")
        self.presetinfo.heading("#0", text="Property")
        self.presetinfo.heading("Value", text="Value")
        current_row +=4

        #Separator
        Separator(self.root,orient="horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')

        self.update_ui()      

        #keep window on top of all others
        self.root.wm_attributes("-topmost", 1)
        self.root.mainloop()

#============================================================#
#=================== Functions ==============================#

    def search(self, *args):
        """search.

        Sets the filter from the search entry field and updates UI
        """
        #get string from entry field and use for filtering database
        self._search_filter = self._entry_text.get()
        self.update_list()
        self.update_ui()        
    
    def save_preset(self):
        """save preset.

        Saves the preset from the selected Reper Track and updates UI.
        If no track is selected, the user is warned.
        """
        #select project and check if a track is selected
        project = reapy.Project()
        if project.n_selected_tracks > 0:
            #open preset dialog and configure setting
            cancelled, result = ui.save_preset_dialog(self.root)
            if not cancelled:
                #get chunk from selected track
                newpreset = rp.save(result[0])
                #create new item and add it to database
                vsti_item = items.vstipreset(result[0], newpreset, result[1])
                self.preset_list[result[0]] = vsti_item
                self.update_list()
            else:
                simpledialog.messagebox.showinfo("Warning", "Please enter Name")
        else:
            simpledialog.messagebox.showinfo("Warning", "Please select Track")

        self.update_ui()
            
    def load_preset(self):
        """load.

        Loads selected preset to selected or new track in Reaper
        """
        #call load function from selected item
        self._selected_item.load()
        self.update_ui()

    def save_database(self):
        """save database.

        Saves the complete database of presets into a binary file with pickle.
        User is asked for folder where to save
        """
        #open file dialog to select database file and pickle data to file
        filename = filedialog.asksaveasfilename(title = "Select file",filetypes = (("database","*.bin"),("all files","*.*")))
        pickle.dump(self.preset_list, open(filename,"wb"))
        self.update_ui()

    def load_database(self):
        """load database.

        Loads a database of presets from a binary file with pickle.
        User is asked for file where to load from
        """
        #open file dialog to select database file and pickle data from file
        filename = filedialog.askopenfilename(title = "Select file",filetypes = (("database","*.bin"),("all files","*.*")))
        self.preset_list = pickle.load( open( filename, "rb" ) )
        self.update_list()
        self.update_ui()

    def new_database(self):
        """new database.

        Creates empty database
        """
        self.preset_list = {}
        self.update_list()
        self.update_ui()

    def select_item(self, evt):
        """select item.

        Event that is called when user clicks on the treeview with the preset

        Parameters
        ----------
            evt: event armgument passed from tkinter
        """
        #get selected item from tree and select from list
        selected_item = self.presettree.item(self.presettree.focus())
        index = selected_item["text"]
        self._selected_item = self.preset_list[index]

        self.update_info()
        self.update_ui()

    def update_info(self):
        """update info.

        Updates info tree with selected item
        """
        #clear all entries in info tree
        self.presetinfo.delete(*self.presetinfo.get_children())
        #check if an item in preset tree is selected
        if self._selected_item != None:
            #loop over properties from selected item and display them in info tree
            for key, value in self._selected_item.properties.items():
                self.presetinfo.insert("", END, text=key, values=(value,))

    def update_list(self):
        """update list.

        Updates preset list from database array
        """
        #clear all entries in preset tree
        self.presettree.delete(*self.presettree.get_children())

        #loop over all items in list
        for preset in self.preset_list:
            #call filter function from item to check if it should be shown
            show = True
            if self._search_filter != "":
                show = self.preset_list[preset].check_filter(self._search_filter)

            #show item based on filter function result
            if show:
                self.presettree.insert("", END, 
                                        text=self.preset_list[preset].preset_name, 
                                        values=(self.preset_list[preset].chunk.plugin_name,))

    def update_ui(self):
        """update UI.

        Updates status of controls based on current selectios
        """

        #check if an item in tree is selected, if not reset internal variable
        if len(self.presettree.selection()) == 0:
            self._selected_item = None

        #enabe or disable save button if there is something in the database
        if len(self.preset_list) == 0:
            self.btn_save_database['state'] = DISABLED
        else:
            self.btn_save_database['state'] = NORMAL

        #enable or disable load button if an item is selected
        if self._selected_item == None:
            self.btn_load_preset['state'] = DISABLED
        else:
            self.btn_load_preset['state'] = NORMAL


#===========================Start Main Function================================#       
mv = main_view()




