import os
import logging
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
    glob.root.wm_attributes("-topmost", 1)
    glob.root.wm_attributes("-topmost", 0)
