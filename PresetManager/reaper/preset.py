# -*- coding: utf-8 -*-
"""Preset Module.

Functions to save and load a preset from/to Reaper

Classes:
    reaper_preset_chunk: class for structuring track chunk

Functions
    save:

Todo:
    * Refactoring to hve cleaner structure

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""
from logging import fatal
import reapy
from reapy.core import track
import rpp
import base64
import logging
import collections
from typing import Dict, List
import core.ui as ui
import core.items as it
import reaper.vsti_list as vsti_list

from base64 import decode

#deriving currently not working
class reaper_preset_chunk():
    """Reaper Prest Chunk.

    Class containing more information about the reaper chunk
    Also wrapping some functions from RPP

    Methods
    -------
        init: init class
        from_element: fill data from RPP state chunk

    Properties
    ----------
        raw: element returned from RPP
        preset_name: Name of preset
        plugin_name: name of plugin that is used in preset
        plugin_dll: name of plugin dll returned from Reaper
        vst_chunk: data from RPP which contain the plugin setting
        trackchunk: complete trackchunk returned from REAPY api
    """

    def __init__(self):
        """Init.

        Initialize all properties
        """
        self.raw = None
        self.type = "Reaper VSTi"
        self.plugin_name = ""
        self.plugin_dll = ""
        self.vst_chunk = ""
        self.track_chunk = ""

    def load(self, new_track=False) -> bool:
        load(self, new_track=new_track)
        return True

    @property
    def properties(self) -> Dict:
        return_dict = {}
        return_dict["DAW"] = "Reaper"
        return return_dict

    def search_tags(self) -> List:
        return ["Reaper"]

    def from_element(self, element, trackchunk = None):
        """From Element.

        Convert RPP elemtent to the state chunk

        Parameters
        ----------
            element: data from RPP
            name: name of preset to be used
            trackchunk: full track chunk from REAPY
        """
        self.raw = element
        self.plugin_name = element.attrib[0]
        self.plugin_dll = element.attrib[1]
        self.vst_chunk = element[:]
        if trackchunk != None:
            self.track_chunk = trackchunk

    def decode_vst_chunk(self):
        base64_message = ''.join(self.vst_chunk[:])

        decoded_chunk = []
        for ch in self.vst_chunk:
            bt = base64.b64decode(ch)
            decoded_chunk.append(bt)

        return decoded_chunk

    def encode_vst_chunk(self, chunk):
        #encode chunk
        encoded_chunk = []
        for ch in chunk:
            bt = base64.b64encode(ch).decode()
            encoded_chunk.append(bt)

        self.vst_chunk = encoded_chunk

def available() -> bool:
    available = False
    project = reapy.Project()
    if project.n_selected_tracks > 0:
        selected_track = project.get_selected_track(0)
        if selected_track.instrument != None:
            available = True

    return available



def save(selected_track = None):
    """Save.

    Saves a preset from selected track in Reaper

    Parameters
    ----------
        presetname: Name of preset to be used

    Returns
    -------
        return_chunk: chunk that can be stored in preset manager
    """
    #get references
    project = reapy.Project()
    if selected_track == None:
        selected_track = project.get_selected_track(0)
    else:
        selected_track = selected_track

    logging.debug('Storing preset from: ' + selected_track.name + "|" + project.name)
    #load configuration from selected track
    vst_track_chunk = reapy.reascript_api.GetTrackStateChunk(selected_track.id,"",10000000,False)
    #parse track state chnk with RPP
    vst_track_chunk_parsed = rpp.loads(vst_track_chunk[2])
    #search for VST plugin data
    preset_chunk = vst_track_chunk_parsed.find("FXCHAIN").find("VST")
    #create new chunk
    return_chunk = reaper_preset_chunk()
    return_chunk.from_element(preset_chunk, vst_track_chunk)

    init_name = selected_track.name

    return return_chunk, init_name

def load(chunk: reaper_preset_chunk, selected_track=None, new_track=False):
    """Load.

    Loads a preset into Reaper

    Parameters
    ----------
        chunk: Chunk to be loaded
    """
    #get references
    project = reapy.Project()

    #check if a track is selected, otherwise create new track
    if new_track == False:
        if selected_track == None:
            if project.n_selected_tracks == 0:
                selected_track = project.add_track(project.n_tracks + 1, "New Track")
            else:
                selected_track = project.get_selected_track(0)
    else:
        selected_track = project.add_track(project.n_tracks + 1, "New Track")

    #chekc if tracks has already an instrument. If so replace if different
    if selected_track.instrument == None: 
        selected_track.add_fx(chunk.plugin_dll)
    elif selected_track.instrument.name != chunk.plugin_name:
        selected_track.instrument.delete()
        selected_track.add_fx(chunk.plugin_dll)

    #read track state from selected track
    vst_track_chunk = reapy.reascript_api.GetTrackStateChunk(selected_track.id,"",10000000,False)
    #parse data with RPP
    vst_track_chunk_parsed = rpp.loads(vst_track_chunk[2])
    
    #add new preset configuration, by replacing portion of the track state
    vst_track_chunk_parsed.find("FXCHAIN").find("VST").children = chunk.vst_chunk
    
    #convert to writeable chunk
    new_chunk = rpp.dumps(vst_track_chunk_parsed)
    #set new chunk to track
    success = reapy.reascript_api.SetTrackStateChunk(selected_track.id, new_chunk,False)
    if success == 1:
        logging.debug('Setting preset to: ' + selected_track.name + "|" + project.name)
    else:
        logging.error('Setting preset to: ' + selected_track.name + "|" + project.name)

def load_vst_chunk(pluginname:str, chunk_string:str, new_track=False):
    """load.

    Loading preset into Reaper.
    """
    new_chunk = chunk_string

    #get ref to project
    project = reapy.Project()
    if project.n_selected_tracks == 0 or new_track == True:
        selected_track = project.add_track(project.n_tracks + 1, "New Track")
        found, plugin = vsti_list.lookup(pluginname)
        if found:
            selected_track.add_fx(plugin.reaper_name)
    else:
        selected_track = project.get_selected_track(0)

    #load chunk from reaper and decode it
    chunk_from_reaper = save(selected_track)[0]
    decoded_chunk_from_reaper = chunk_from_reaper.decode_vst_chunk()

    
    selected_track.instrument.delete()
    selected_track.add_fx(chunk_from_reaper.plugin_dll)

    

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
    load(chunk_from_reaper, selected_track)