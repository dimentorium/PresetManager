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
from typing import Dict, List
import reaper.preset as rp
import core.ui as ui
from tkinter import simpledialog, filedialog
from playsound import playsound
from openal import *
import threading
import time
import logging
import reapy
import sys

import base64
import reaper.preset as rpre
from reaper import vsti_list

class preset_data_base():
    """Preset Data class.

    Base class for preset data that should be overriden by custom implementation
    
    Methods
    -------
        init: init class and set properties
        properties: returns a list of all properties that should be displayed in the property tree
        search_tags: list of tags that are used for searching
        load: function that is called for loading
        save: function that is called for saving

    Properties
    ----------
    """

    def __init__(self) -> None:
        """Init function to be overriden
        """
        self.plugin_name = ""
        self.type = ""
        pass

    @property
    def properties(self) -> Dict:
        """Properties function to be overriden

        Returns:
            Dict: list of custom properties
        """
        return {}

    def search_tags(self) -> List:
        """Search Tags function to be overriden

        Returns:
            List: list of custom search tags
        """
        return []

    def load(self) -> bool:
        """Load function to be overriden

        Returns:
            bool: success
        """
        return False


class list_item():
    """List item.

    Class for handling the usage and displaying of presets in the presets manager
    Custom imlementations are set within the chunk

    Methods
    -------
        init: init class and set properties
        properties: returns a list of all properties that should be displayed in the property tree
        search_tags: returns a list of all tags that can be searched
        check_filter: function to check if the item should be shown when searching is used
        load: call specific load function from chunk
        play: play preview file

    Properties
    ----------
        preset_name: Name of preset
        chunk: specific chunk data based on preset_data_base
        plugin_name: name of plugin from chunk
        type: type of preset from chunk
        tags: list of strings for the tag list
        preview_path: path to audio preview
        rating: rating of preset from 1-5
        favorite: mark preset as favorite
    """  
    def __init__(self, preset_name: str, chunk: preset_data_base, tags = []) -> None:
        """Init.

        Initialize class properties.
        
        Parameters
        ----------
            preset_name: name string for preset
            chunk: specific chunk data based on preset_data_base
            tags: list of strings for the tag list
        """
        self.preset_name = preset_name
        self.chunk = chunk
        self.plugin_name = self.chunk.plugin_name
        self.type = self.chunk.type
        self.tags = tags
        self.preview_path = ""
        self.rating = 0
        self.favorite = False

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
        props["Plugin Name"] = self.plugin_name
        props["Tags"] = self.tags
        props["Preview"] = self.preview_path
        props["Rating"] = self.rating
        props["Favorite"] = self.favorite
        #add properties from custom chunk implementation
        props.update(self.chunk.properties)
        return props

    def search_tags(self) -> List:
        st = []
        st.append(self.plugin_name)
        st.append(self.type)
        st.extend(self.tags)
        st.append("Rate: " + str(self.rating))
        st.append("Favorite: " + str(self.favorite))
        #add tags from custom implementation
        st.extend(self.chunk.search_tags())
        return st

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
        show_plugin = filter in self.plugin_name
        show_tags = filter in self.tags
        show_rating = filter == str(self.rating)
        show_favorite = (filter == "fav") and self.favorite
        show = show_name or show_tags or show_plugin or show_rating or show_favorite
        return show

    def load(self) -> bool:
        """load.

        Loading preset into Reaper.
        """
        result = self.chunk.load()
        return result
  
    def play(self):
        """Play sound.

        Play audio preview if available
        """
        #check that there is a correct path for playing audio
        if self.preview_path != "":
            try:
                if self.preview_path.endswith(".ogg"):
                    #play ogg
                    logging.debug("Playing: " + self.preview_path)
                    t = threading.Thread(target=self.play_ogg, args=(self.preview_path,))
                    t.start()
                    
                else:
                    #play audio wav or mp3
                    logging.debug("Playing: " + self.preview_path)
                    playsound(self.preview_path, block=False)
            except:
                        e = sys.exc_info()[0]
                        logging.debug("Could not play:" + self.preview_path)

    def play_ogg(self, filename):
        """Play ogg file
        Helper function to be called as background thread to play ofgg file

        Arguments:
            filename {string} -- full path to ogg file to be played
        """
        source = oalOpen(self.preview_path)
        source.play()
        while source.get_state() == AL_PLAYING:
            time.sleep(1)
        #causing issues so diabled it
        #oalQuit()