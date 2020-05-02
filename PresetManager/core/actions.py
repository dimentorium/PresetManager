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

import core.globals as glob
import core.items as items


def save_preset():
    """Save preset.

    Saves the preset from the selected Reaper Track and updates UI.
    If no track is selected, the user is warned.
    """
    newitem = items.vstipreset()
    if newitem.save():
        logging.debug('Saving Preset: ' + newitem.preset_name)

def show():
    """Show.

    Brings Preset Manager Window to front
    """
    glob.root.wm_attributes("-topmost", 1)
    glob.root.wm_attributes("-topmost", 0)
