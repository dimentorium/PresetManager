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
import reapy
from reapy.core import track
import rpp
import base64

class reaper_preset_chunk:
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
        self.preset_name = "Preset"
        self.plugin_name = ""
        self.plugin_dll = ""
        self.vst_chunk = ""
        self.track_chunk = ""

    def from_element(self, element, name: str, trackchunk = None):
        """From Element.

        Convert RPP elemtent to the state chunk

        Parameters
        ----------
            element: data from RPP
            name: name of preset to be used
            trackchunk: full track chunk from REAPY
        """
        self.raw = element
        self.preset_name = name
        self.plugin_name = element.attrib[0]
        self.plugin_dll = element.attrib[1]
        self.vst_chunk = element[:]
        if trackchunk != None:
            self.track_chunk = trackchunk


def save(presetname: str) -> reaper_preset_chunk:
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
    selected_track = project.get_selected_track(0)

    #load configuration from selected track
    vst_track_chunk = reapy.reascript_api.GetTrackStateChunk(selected_track.id,"",500000,False)
    
    #parse track state chnk with RPP
    vst_track_chunk_parsed = rpp.loads(vst_track_chunk[2])

    #search for VST plugin data
    preset_chunk = vst_track_chunk_parsed.find("FXCHAIN").find("VST")

    #create new chunk
    return_chunk = reaper_preset_chunk()
    return_chunk.from_element(preset_chunk,presetname, vst_track_chunk)

    return return_chunk

def load(chunk: reaper_preset_chunk):
    """Load.

    Loads a preset into Reaper

    Parameters
    ----------
        chunk: Chunk to be loaded
    """
    #get references
    project = reapy.Project()
    selected_track = None

    #check if a track is selected, otherwise create new track
    if project.n_selected_tracks == 0:
        selected_track = project.add_track(project.n_tracks + 1, "New Track")
    else:
        selected_track = project.get_selected_track(0)

    #chekc if tracks has already an instrument. If so replace if different
    if selected_track.instrument == None: 
        selected_track.add_fx(chunk.plugin_dll)
    elif selected_track.instrument.name != chunk.plugin_name:
        selected_track.instrument.delete()
        selected_track.add_fx(chunk.plugin_dll)

    #read track state from selected track
    vst_track_chunk = reapy.reascript_api.GetTrackStateChunk(selected_track.id,"",500000,False)
    #parse data with RPP
    vst_track_chunk_parsed = rpp.loads(vst_track_chunk[2])
    
    #add new preset configuration, by replacing portion of the track state
    vst_track_chunk_parsed.find("FXCHAIN").find("VST").children = chunk.vst_chunk
    
    #convert to writeable chunk
    new_chunk = rpp.dumps(vst_track_chunk_parsed)
    #set new chunk to track
    reapy.reascript_api.SetTrackStateChunk(selected_track.id,new_chunk,False)