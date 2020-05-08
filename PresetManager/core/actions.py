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
            glob.main_window.update_list()
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
        glob.main_window.update_ui()

def show():
    """Show.

    Brings Preset Manager Window to front
    """
    glob.root.wm_attributes("-topmost", 1)
    glob.root.wm_attributes("-topmost", 0)
