# -*- coding: utf-8 -*-
"""UI Package.

This package contains UI modules for the preset manager

Modules:

Todo:
    *

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""
import core.items as items
from core.ui import edit_preset, startup, main

def start_main(command_queue):
    main.main_view(command_queue)

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
    database_dialog = startup.startup_dialog()
    new_database = database_dialog.new
    return new_database

def edit_preset_dialog(preset: items.vstipreset):
    """Save Preset Dialog.

    Wrapper function showing dialog and returning data

    Parameters
    ----------
        parent: root frame calling dialog
        
    Returns:
    -------
        OK: True if dialog was achknowledged
        result: list with preset name and list of tags
    """
    #call dialog and read out returning values
    save_dialog = edit_preset.Edit_Preset(preset)
    OK = not save_dialog.cancelled
    return OK
