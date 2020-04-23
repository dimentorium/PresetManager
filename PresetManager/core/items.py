# -*- coding: utf-8 -*-
"""Items module.

Contains classes for items that are displayed by the preset tree. 
With this abstraction layer different elements can be displayed and
connected to reaper

Classes:
    vstipreset: class for handling vsti presets

Functions

Todo:
    * Refactoring to hve cleaner structure

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""

import collections
import reaper.preset as rp
import core.ui as ui
from tkinter import simpledialog, filedialog
from playsound import playsound



class vstipreset():
    """vstipreset.

    Class for handling the usage and displaying of VSTi presets in the presets manager
    All other items should implement the same functions

    Methods
    -------
        init: init class and set properties
        properties: returns a list of all properties that should be displayed in the property tree
        check_filter: function to check if the item should be shown when searching is used
        load: handles loading of vstipreset into Reaper
        save: handles savin of vstipreset from Reaper
        onclick: action that is performed when vstipreset is selected
        ondoubleclick: action that is performed when vstipreset is doubleclicked

    Properties
    ----------
        preset_list: list of all presets, database
    """

    def __init__(self, preset_name = "", chunk = None, tags = []) -> None:
        """Init.

        Initialize class properties.
        
        Parameters
        ----------
            preset_name: name string for preset
            chunk: chunk that is stored for Reaper
            tags: list of strings for the tag list
        """
        self.preset_name = preset_name
        self.type = "VSTi Preset"
        self.chunk = chunk
        self.tags = tags
        self.preview_path = ""

    @property
    def properties(self) -> collections.OrderedDict:
        """properties.

        Returns ordered dict with list of properties.
        
        Returns
        -------
            props: ordered dict with list of properties to be displayed
        """
        props = collections.OrderedDict()
        props["Preset Name"] = self.preset_name
        props["Type"] = self.type
        props["Plugin Name"] = self.chunk.plugin_name
        props["Tags"] = self.tags
        props["Preview"] = self.preview_path
        return props

    def check_filter(self, filter: str) -> bool:
        """check_filter.

        Check string filter for item to determine if it is to be shown
        
        Parameters
        ----------
            filter: search string

        Returns
        -------
            show: boolean return if item has search string
        """
        show_name = filter in self.preset_name
        show_plugin = filter in self.chunk.plugin_name
        show_tags = filter in self.tags
        show = show_name or show_tags or show_plugin
        return show

    def load(self):
        """load.

        Loading preset into Reaper.
        """
        rp.load(self.chunk)
        

    def save(self) -> bool:
        """save.

        Saving presets from Reaper.
        """
        result = False
        self.chunk = rp.save()
        if self.chunk is not None:
            #open preset dialog and configure setting
            cancelled = ui.save_preset_dialog(self)
            if not cancelled:
                result = True
        else:
            simpledialog.messagebox.showinfo("Warning", "Please select Track")

        return result
            

    def onclick(self):
        """onclick.

        Action when item is selected. Play Audio
        """
        #check that there is a correct path for playing audio
        if self.preview_path != "":
            #play audio
            try:
                playsound(self.preview_path, block=False)
            except:
                print("Could not play:" + self.preview_path)

    def ondoubleclick(self):
        """ondoubleclick.

        Action when item is double clicked.
        """
        pass


