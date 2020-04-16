import reapy
from reapy.core import track
import rpp
import base64
import pandas as pd

class reaper_preset_chunk:
    def __init__(self):
        self.raw = None
        self.preset_name = "Preset"
        self.plugin_name = ""
        self.plugin_dll = ""
        self.vst_chunk = ""
        self.track_chunk = ""

    def from_element(self, element, name, trackchunk = None):
        self.raw = element
        self.preset_name = name
        self.plugin_name = element.attrib[0]
        self.plugin_dll = element.attrib[1]
        self.vst_chunk = element[:]
        if trackchunk != None:
            self.track_chunk = trackchunk


def save(presetname):
    #get references
    project = reapy.Project()
    selected_track = project.get_selected_track(0)

    #load configuration from first track
    vst_track_chunk = reapy.reascript_api.GetTrackStateChunk(selected_track.id,"",500000,False)
    vst_track_chunk_parsed = rpp.loads(vst_track_chunk[2])
    preset_chunk = vst_track_chunk_parsed.find("FXCHAIN").find("VST")
    return_chunk = reaper_preset_chunk()
    return_chunk.from_element(preset_chunk,presetname, vst_track_chunk)

    return return_chunk

def load(chunk):
    #get references
    project = reapy.Project()
    selected_track = None

    if project.n_selected_tracks == 0:
        selected_track = project.add_track(project.n_tracks + 1, "New Track")
    else:
        selected_track = project.get_selected_track(0)

    if selected_track.instrument == None: 
        selected_track.add_fx(chunk.plugin_dll)
    elif selected_track.instrument.name != chunk.plugin_name:
        #todo delete existing
        selected_track.instrument.delete()
        selected_track.add_fx(chunk.plugin_dll)


    vst_track_chunk = reapy.reascript_api.GetTrackStateChunk(selected_track.id,"",500000,False)
    vst_track_chunk_parsed = rpp.loads(vst_track_chunk[2])
    
    #add new preset configuration
    vst_track_chunk_parsed.find("FXCHAIN").find("VST").children = chunk.vst_chunk
    
    #convert to writeable chunk
    new_chunk = rpp.dumps(vst_track_chunk_parsed)
    #set new chunk
    reapy.reascript_api.SetTrackStateChunk(selected_track.id,new_chunk,False)

def chunk_to_row(chunk: reaper_preset_chunk):
    chunk_series = pd.Series([chunk.preset_name, chunk.plugin_name, chunk.plugin_dll, chunk.vst_chunk], index=["presetname","pluginname","plugindll","chunk"])
    return chunk_series