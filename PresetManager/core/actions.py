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
from core.item_list import update
import core.items as items
import reaper.preset as rp
import core.ui as ui
import core.item_list as item_list
import core.tags as tags

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
            tags.update(new_item.tags)
            tags.save()
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
    #update_ui()

def edit_preset(evt):
    """Edit Preset

    Edits the currently selected preset by calling the editor

    Arguments:
        evt {event} -- Event Reference needed from TKInter but not used in code
    """
    #check if a preset is selected
    selected_preset = glob.main_window._selected_item
    if selected_preset != None:
        #call dialog to edit preset
        if ui.edit_preset_dialog(selected_preset):
            logging.debug('Editing Preset: ' + selected_preset.preset_name)
            item_list.update(selected_preset)
            #check if tags are already in list
            tags.update(selected_preset.tags)
            tags.save()
            #update user interface
            update_ui()
        else:
            logging.debug('Cancel Editing Preset: ' + selected_preset.preset_name)
    else:
        logging.debug('No Preset selected')
        simpledialog.messagebox.showinfo("Warning", "Please select Preset")

def import_presets():
    """Import presets from Folder

    Currently experimental function for loading NKSF files
    directly into the preset manager
    """
    #ask user to select folder for presets
    folder = filedialog.askdirectory(title="Select Directory")

    if os.path.exists(folder):
        logging.debug('Starting import: %s', folder)
        #loop over files, not yet recursively
        for filename in os.listdir(folder):
            #if it is an nksf file, add it to list and update presets
            if filename.endswith(".nksf"):
                logging.debug('Import: %s', filename)
                preset_to_add = items.nksfpreset(os.path.join(folder, filename))

                #check for preview
                preview_file = folder + "\\.previews\\" + filename + ".ogg"
                if os.path.exists(preview_file):
                    preset_to_add.preview_path = preview_file

                item_list.add(preset_to_add)
                tags.update(preset_to_add.tags)
        tags.save()
        update_ui()
    elif folder == "":
        #user cancelled dialog
        logging.debug('Import cancelled')

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

    update_ui()

def new_database():
    """new database.

    Creates empty database
    """
    filename = filedialog.asksaveasfilename(initialfile="database.bin", title="Select database file", filetypes=(("database", "*.bin"), ("all files", "*.*")))

    #check if file exists already
    if os.path.exists(filename):
        logging.debug('Overwriting Database: %s', filename)
        item_list.new(filename)
    elif filename == "":
        #user cancelled dialog
        logging.debug('Create database cancelled')
    else:
        logging.debug('Creating Database: %s', filename)
        item_list.new(filename)
    
    update_ui()

def load_database():
    """Load database.

    Loads a database of presets from a binary file with pickle.
    User is asked for file where to load from
    """
    #open file dialog to select database file and pickle data from file
    filename = filedialog.askopenfilename(title="Select file", filetypes=(("database", "*.bin"), ("all files", "*.*")))

    #Check if file exists and load it, this should be handled by OS dialog
    if os.path.exists(filename):
        logging.debug('Loading Database: %s', filename)
        item_list.load(filename)
        update_ui()
    elif filename == "":
        #user cancelled dialog
        logging.debug('Load database cancelled')
    else:
        logging.debug('Database file not existing: %s', filename)
        simpledialog.messagebox.showerror("File Error", "Please select database file")

def save_database():
    """Save database.

    Saves the complete database of presets into a binary file with pickle.
    User is asked for folder where to save
    """
    filename = filedialog.asksaveasfilename(initialdir=item_list.folder_name(), initialfile=item_list.file_name(), title="Select file", filetypes=(("database", "*.bin"), ("all files", "*.*")))

    if filename == "":
        #user cancelled dialog
        logging.debug('Save database cancelled')
    else:
        #check if new path is selected and update database accordingly
        if os.path.normpath(filename) != item_list.file_path():
            logging.debug('Changing Database Path: %s', filename)
            item_list.set_file_path(filename)

        logging.debug('Saving Database: %s', item_list.file_path())
        item_list.save()
        update_ui()


#============================================================#
#=================== UI Handling ============================#

def update_ui():
    """Update Main View.

    Calls View functions to update the Main Window
    """
    glob.main_window.update_list()
    glob.main_window.update_info()
    glob.main_window.update_ui()

def show():
    """Show.

    Brings Preset Manager Window to front
    """
    #glob.root.wm_attributes("-topmost", 0)
    glob.root.deiconify()
    glob.root.wm_attributes("-topmost", 1)
