import os
import logging
import queue

from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog, filedialog

import textwrap

import pickle

import core.globals as glob
from logging import disable
import reaper.preset as rp
import reapy
import core.ui as ui
import core.items as items
from core import tags, item_list, actions
from reaper import server
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
    
    def __init__(self, command_queue: queue.Queue):
        """Init.

        Initialize class properties.
        Builds window and links function calls
        """
        logging.debug("Starting Main UI")
        self._search_filter = ""
        self._selected_item = None
        self.__command_queue = command_queue
        
        self.root = Tk()
        self.root.title("Reaper Preset Manager")

        s = Style()
        #s.configure("TButton", padding=6, relief="flat", background="#ccc")
        #s.configure('new.TFrame', background='#707070')
        #s.configure("TLabel", padding=5, relief="flat", background="#707070")

        

        #build menu
        """
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Database", command=actions.new_database)

        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)
        """

        #Build UI
        self._frame = Frame(self.root, style='new.TFrame')
        self._frame.grid(row=0, column=0, sticky=E+W+N+S)
        
        current_row = 0

        #Buttons for handling database
        self.btn_new_database = Button(self._frame,text="New Database", command=actions.new_database)
        self.btn_new_database.grid(row=current_row,column=0, padx=5, pady=5, sticky='ew')

        self.btn_load_database = Button(self._frame,text="Load Database", command=actions.load_database)
        self.btn_load_database.grid(row=current_row,column=1, padx=5, pady=5, sticky='ew')

        self.btn_save_database = Button(self._frame,text="Save Database", command=actions.save_database)
        self.btn_save_database.grid(row=current_row,column=2, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Database Name
        Label(self._frame,text="Database").grid(row=current_row, padx=5, column=0, sticky='w')
        self.lbl_database = Label(self._frame, relief=GROOVE)
        self.lbl_database.grid(row=current_row, column=1, columnspan=4, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Separator
        Separator(self._frame,orient="horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Buttons for handling presets
        self.btn_load_preset = Button(self._frame,text="Set Preset", command=actions.load_preset)
        self.btn_load_preset.grid(row=current_row,column=0, padx=5, pady=5, sticky='ew')
        
        self.btn_save_preset = Button(self._frame,text="Get Preset", command=actions.save_preset)
        self.btn_save_preset.grid(row=current_row,column=1, padx=5, pady=5, sticky='ew')

        self.btn_import_folder = Button(self._frame,text="Import Folder", command=actions.import_presets)
        self.btn_import_folder.grid(row=current_row,column=2, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Separator
        Separator(self._frame,orient="horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Search Field
        Label(self._frame,text="Search").grid(row=current_row, padx=5, column=0, sticky='w')
        
        self._entry_text = StringVar()
        self._entry_text.trace("w", self.search)
        self.search_box = Entry(self._frame, textvariable=self._entry_text)
        self.search_box.grid(row=current_row, column=1,columnspan=3, padx=5, pady=5, sticky='ew')
        current_row += 1

        #Separator
        Separator(self._frame, orient="horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')
        current_row += 1

        #Treeview for presets
        self.presettree = Treeview(self._frame)
        self.presettree.grid(row=current_row, rowspan=8, columnspan=3, padx=5, pady = 5, sticky = 'ew')
        self.presettree.bind("<<TreeviewSelect>>", self.select_item)
        self.presettree.bind("<Double-1>", actions.edit_preset)
        self.presettree["columns"] = ("Plugin")
        self.presettree.heading("#0", text="Preset")
        self.presettree.heading("Plugin", text="Plugin")
        vsb = Scrollbar(self._frame, orient="vertical", command=self.presettree.yview)
        vsb.grid(row = current_row, rowspan = 8, column = 3, pady = 5, sticky ='nsw')
        self.presettree.configure(yscrollcommand = vsb.set)
        current_row += 8

        #Treeview for presets
        self.presetinfo = Treeview(self._frame)
        self.presetinfo.grid(row=current_row, rowspan=2, columnspan=3, padx=5, pady=5, sticky='nesw')
        self.presetinfo["columns"] = ("Value")
        self.presetinfo.heading("#0", text="Property")
        self.presetinfo.heading("Value", text="Value")
        current_row += 4

        #Separator
        Separator(self._frame, orient = "horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')

        self.update_ui()  

        for i in range(0, 4):
            self._frame.columnconfigure(i, weight=1)

        for i in range(0, 17):
            self._frame.rowconfigure(i, weight=1)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        #set gobals
        glob.root = self.root
        glob.main_window = self

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #start window on top of all others
        #self.root.wm_attributes("-topmost", 1)

        logging.debug('Starting Mainloop')
        #call new database after half second to select
        self.root.after(500, actions.select_database)
        self.root.after(500, self.process_incoming)
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
        self._selected_item = item_list.get()[index]
        self._selected_item.onclick()

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
                if key != "Tags":
                    self.presetinfo.insert("", END, text=key, values=(value,))
            
            alltags = self._selected_item.properties["Tags"]
            tags_entry = self.presetinfo.insert("", END, text="Tags", values=(len(alltags),))
            for prop in alltags:
                self.presetinfo.insert(tags_entry, END, text="", values=(prop,))
            
            self.presetinfo.item(tags_entry, open=True)

    def update_list(self):
        """update list.

        Updates preset list from database array
        """
        #clear all entries in preset tree
        self.presettree.delete(*self.presettree.get_children())

        #loop over all items in list
        for preset in item_list.get():
            #call filter function from item to check if it should be shown
            show = True
            if self._search_filter != "":
                show = item_list.get()[preset].check_filter(self._search_filter)

            #show item based on filter function result
            if show:
                self.presettree.insert("", END, 
                                        text=item_list.get()[preset].preset_name, 
                                        values=(item_list.get()[preset].plugin_name,))
        
        self.update_ui()

    def update_ui(self):
        """update UI.

        Updates status of controls based on current selectios
        """
        if item_list.initialized():
            self.lbl_database['text'] = item_list.file_path()
            self.btn_save_preset['state'] = NORMAL
            self.btn_import_folder['state'] = NORMAL

            #check if an item in tree is selected, if not reset internal variable
            if len(self.presettree.selection()) == 0:
                self._selected_item = None

            #enabe or disable save button if there is something in the database
            if len(item_list.get()) == 0:
                self.btn_save_database['state'] = DISABLED
            else:
                self.btn_save_database['state'] = NORMAL

            #enable or disable load button if an item is selected
            if self._selected_item == None:
                self.btn_load_preset['state'] = DISABLED
            else:
                self.btn_load_preset['state'] = NORMAL

        else:
            self.btn_load_preset['state'] = DISABLED
            self.btn_save_preset['state'] = DISABLED
            self.btn_import_folder['state'] = DISABLED
            self.btn_save_database['state'] = DISABLED

    def on_closing(self):
        logging.debug('Exiting application clicked')
        result = simpledialog.messagebox.askyesnocancel("Quit", "Do you want to save the database?")
        if result == None:
            logging.debug('Exiting cancelled')
        elif result == True:
            logging.debug('Saving database')
            actions.save_database()
            logging.debug('Exiting application')
            self.root.destroy()
        else:
            logging.debug('Exiting application')
            self.root.destroy()

    def process_incoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.__command_queue.qsize():
            try:
                message = self.__command_queue.get()
                if message == "save_preset":
                    actions.show()
                    actions.save_preset()
                elif message == "show":
                    actions.show()
            except queue.Empty:
                pass
        self.root.after(1000, self.process_incoming)
