import reapy
from reapy.core import track
import rpp
import base64
import reaper.preset as rpre
import core.preset.fxp as fxp
import os

#load chunk from reaper and decode it
chunk_from_reaper = rpre.save()
decoded_chunk_from_reaper = chunk_from_reaper.decode_vst_chunk()

presetpath = r"C:\Users\phili\Desktop\fxp\Tyrell"

for filename in os.listdir(presetpath):
    #read nks file and get chunk
    fxppreset = fxp.FXPPreset(os.path.join(presetpath, filename))
    new_chunk = fxppreset.fxpchunk

    #convert chunk into list with length 210
    length = 210
    progchunk = [new_chunk[i:i+length] for i in range(0, len(new_chunk), length)]

    #insert reaper specific header and footer
    progchunk.insert(0, decoded_chunk_from_reaper[0])
    pgm_name = b'\x00' + "test".encode() + b'\x00\x10\x00\x00\x00'
    progchunk.append(pgm_name)
    

    chunktest1 = rpre.save().decode_vst_chunk()
    #load new chunk into reaper
    chunk_from_reaper.encode_vst_chunk(progchunk)
    rpre.load(chunk_from_reaper)

    #todo validate
    chunktest2 = rpre.save().decode_vst_chunk()
    if chunktest1==chunktest2:
        print("Failed: " + filename)
    else:
        print("Success: " + filename)