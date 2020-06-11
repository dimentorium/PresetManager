# -*- coding: utf-8 -*-
"""FXP Package.

This package contains modules for importing FXP files

Modules:

Todo:
    *

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""
import os
import logging

import core.item_list as item_list
import core.tags as tags
import core.items as items
from Importer.NKSF import file

def load_file(filepath: str):
    """Load NKSF file

    Args:
        filepath (str): full path for nksf file to load

    Returns:
        NKSF_file: object containing all NKSF data
    """
    nksf_file = file.NKSF_file(filepath, True, True, True)
    return nksf_file

def import_folder(foldername:str):
    """Import NKSF presets from Folder.

    Currently experimental function for loading NKSF files
    directly into the preset manager
    """
    #ask user to select folder for presets
    folder = foldername

    if os.path.exists(folder):
        logging.debug('Starting import: %s', folder)
        #loop over files, not yet recursively
        for filename in os.listdir(folder):
            #if it is an nksf file, add it to list and update presets
            if filename.endswith(".nksf"):
                logging.debug('Import: %s', filename)
                nksf_data = load_file(os.path.join(folder, filename))
                preset_to_add = items.list_item(nksf_data.preset_name,nksf_data, nksf_data.tags)

                #check for preview
                preview_file = folder + "\\.previews\\" + filename + ".ogg"
                if os.path.exists(preview_file):
                    preset_to_add.preview_path = preview_file

                item_list.add(preset_to_add)
                tags.update(preset_to_add.tags)
    elif folder == "":
        #user cancelled dialog
        logging.debug('Import cancelled')