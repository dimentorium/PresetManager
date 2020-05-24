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
import librosa
import simpleaudio as sa
from openal import *
import threading
import time
import logging
import reapy
import sys

import base64
import reaper.preset as rpre
import core.preset.nksf as nksf



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
        self.plugin_name = self.chunk.plugin_name
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
        props["Plugin Name"] = self.chunk.plugin_name
        props["Tags"] = self.tags
        props["Preview"] = self.preview_path
        props["Rating"] = self.rating
        props["Favorite"] = self.favorite
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
        show_plugin = filter in self.plugin_name
        show_tags = filter in self.tags
        show_rating = filter == str(self.rating)
        show_favorite = (filter == "fav") and self.favorite
        show = show_name or show_tags or show_plugin or show_rating or show_favorite
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
            cancelled = ui.edit_preset_dialog(self)
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
                logging.debug("Playing: " + self.preview_path)
                playsound(self.preview_path, block=False)
            except:
                logging.debug("Could not play:" + self.preview_path)

    def ondoubleclick(self):
        """ondoubleclick.

        Action when item is double clicked.
        """
        pass

class nksfpreset():
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

    def __init__(self, filepath = "") -> None:
        """Init.

        Initialize class properties.
        
        Parameters
        ----------
            preset_name: name string for preset
            chunk: chunk that is stored for Reaper
            tags: list of strings for the tag list
        """
        self.filepath = filepath
        preset_to_convert = nksf.NKSF(self.filepath, True, True, True)

        self.preset_name = preset_to_convert.name
        self.type = "NKSF Preset"
        self.tags = preset_to_convert.tags
        self.plugin_name = preset_to_convert.pluginname
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
        show_plugin = filter in self.plugin_name
        show_tags = filter in self.tags
        show = show_name or show_tags or show_plugin
        return show

    def load(self):
        """load.

        Loading preset into Reaper.
        """
        #load chunk from reaper and decode it
        chunk_from_reaper = rpre.save()
        decoded_chunk_from_reaper = chunk_from_reaper.decode_vst_chunk()

        project = reapy.Project()
        selected_track = project.get_selected_track(0)
        selected_track.instrument.delete()
        selected_track.add_fx(chunk_from_reaper.plugin_dll)

        #read nks file and get chunk
        preset_to_convert = nksf.NKSF(self.filepath, True, True, True)
        new_chunk = preset_to_convert._NKSF__chunks["PCHK"].data

        #convert chunk into list with length 210
        length = 210
        presetdata = [new_chunk[i:i+length] for i in range(0, len(new_chunk), length)]

        #insert reaper specific header and footer
        """This is used to calculate the number of list elements for the header of the fx state chunk
        it is built up the following:
        4 Bytes: VST ID
        4 Bytes: Reaper Magix Number
        4 Bytes: Number of Inputs
        8 Bytes by Number of inputs: Input Mask
        4 Bytes: Number of outputs
        8 Bytes by Number of outputs: output Mask
        4 Bytes: Something I don't know
        8 Bytes: seems to be the end 01 00 00 00 00 00 10 00
        """
        instrument_description_lenth = 4 + 4 + 4 + (selected_track.instrument.n_inputs * 8) + 4 + (selected_track.instrument.n_outputs * 8) + 4 + 8
        # calculate number of list elements needed for length. Per element its 210 bytes
        no_list_elements = int(instrument_description_lenth / 210) + (instrument_description_lenth % 210 > 0)

        if no_list_elements == 1:
            progchunk = [decoded_chunk_from_reaper[0]] + presetdata
        else:
            progchunk = decoded_chunk_from_reaper[0:no_list_elements-1] + presetdata
        pgm_name = b'\x00' + "test".encode() + b'\x00\x10\x00\x00\x00'
        progchunk.append(pgm_name)

        #load new chunk into reaper
        chunk_from_reaper.encode_vst_chunk(progchunk)
        rpre.load(chunk_from_reaper)

        

    def save(self) -> bool:
        """save.

        Saving presets from Reaper.
        """
        result = False
        self.chunk = rp.save()
        if self.chunk is not None:
            #open preset dialog and configure setting
            cancelled = ui.edit_preset_dialog(self)
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
                logging.debug("Playing: " + self.preview_path)
                t = threading.Thread(target=self.play_ogg, args=(self.preview_path,))
                t.start()
            except:
                e = sys.exc_info()[0]
                logging.debug("Could not play:" + self.preview_path)

    def ondoubleclick(self):
        """ondoubleclick.

        Action when item is double clicked.
        """
        pass

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



