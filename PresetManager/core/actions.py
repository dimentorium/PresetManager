# -*- coding: utf-8 -*-
"""Actions module.

Contains functions that are called by UI or command server

Functions

Todo:

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""

import os
import logging

from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog, filedialog

import core.globals as glob
import core.items as items
import reaper.preset as rp
import core.ui as ui
import core.item_list as item_list

#============================================================#
#=================== Preset Handling ========================#
def save_preset():
    """Save preset.

    Saves the preset from the selected Reaper Track and updates UI.
    If no track is selected, the user is warned.
    """
    preset_available = rp.available()

    if preset_available:
        new_preset = rp.save()

        new_item = items.vstipreset("New Preset", new_preset)
        if ui.edit_preset_dialog(new_item):
            logging.debug('Saving Preset: ' + new_item.preset_name)
            item_list.add(new_item)
            update_ui()
    else:
        logging.debug('No Preset available')
        simpledialog.messagebox.showinfo("Warning", "Please select appropriate Track")

def load_preset():
    """load.

    Loads selected preset to selected or new track in Reaper
    """
    #call load function from selected item
    glob.main_window._selected_item.load()
    logging.debug('Loading Preset: ' + glob.main_window._selected_item.preset_name)
    update_ui()

#============================================================#
#=================== Database Handling ======================#
def select_database():
    """Select database.

    Asks user to load or create a databas
    """
    create_new_database = ui.new_database_dialog()
    if create_new_database:
        logging.debug("User selected new database")
        new_database()
    else:
        logging.debug("User selected load database")
        load_database()

def new_database():
    """new database.

    Creates empty database
    """
    filename = filedialog.asksaveasfilename(initialfile="database.bin", title="Select database file", filetypes=(("database","*.bin"),("all files","*.*")))

    if os.path.exists(filename):
        logging.debug('Overwriting Database: ' + filename)
        item_list.load(filename)
        update_ui()
    else:
        logging.debug('Creating Database: ' + filename)
        item_list.new(filename)
        update_ui()

def load_database():
    """Load database.

    Loads a database of presets from a binary file with pickle.
    User is asked for file where to load from
    """
    #open file dialog to select database file and pickle data from file
    filename = filedialog.askopenfilename(title="Select file", filetypes=(("database","*.bin"),("all files","*.*")))

    #Check if file exists and load it, this should be handled by OS dialog
    if os.path.exists(filename):
        logging.debug('Loading Database: ' + filename)
        item_list.load(filename)
        update_ui()
    else:
        logging.debug('Database file not existing: ' + filename)
        simpledialog.messagebox.showerror("File Error", "Please select database file")

def save_database():
    """Save database.

    Saves the complete database of presets into a binary file with pickle.
    User is asked for folder where to save
    """
    filename = filedialog.asksaveasfilename(initialdir=item_list.LIST_FOLDER, initialfile=item_list.LIST_FILE, title="Select file", filetypes=(("database","*.bin"),("all files","*.*")))

    if os.path.normpath(filename) != item_list.file_path():
        logging.debug('Changing Database Path: ' + filename)
        item_list.set_file_path(filename)

    logging.debug('Saving Database: ' + item_list.file_path())
    item_list.save()
    update_ui()


#============================================================#
#=================== UI Handling ============================#

def update_ui():
    """Update Main View.

    Calls View functions to update the Main Window
    """
    glob.main_window.update_list()
    glob.main_window.update_ui()

def show():
    """Show.

    Brings Preset Manager Window to front
    """
    glob.root.wm_attributes("-topmost", 1)
    glob.root.wm_attributes("-topmost", 0)
