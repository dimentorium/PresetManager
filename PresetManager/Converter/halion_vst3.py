import reapy
from reapy.core import track
import rpp
import base64
import reaper.preset as rpre
import Converter.vstpreset as vsti

#load chunk from reaper
reaper_chunk_raw = rpre.save("test")

#convert base64 chunk to bytes
reaper_chunk_dec = []
reaper_string_dec = bytes()
for ch in reaper_chunk_raw.vst_chunk:
    bt = base64.b64decode(ch)
    reaper_chunk_dec.append(bt)
    reaper_string_dec += bt

#load vstipreset
vstipreset = vsti.VSTPreset("C:\\Users\\phili\\Desktop\\Amped Mark 1.vstpreset")
#vstipreset = vsti.VSTPreset("C:\\Users\\phili\\Desktop\\Halion\\Multi\\[GM 001] Acoustic Grand Piano.vstpreset")

#extract chunk from vstipreset
vsti_chunk_loaded = vstipreset.chunklist[0].data
vsti_chunk_loaded = vsti_chunk_loaded + vstipreset.chunklist[1].data
#vsti_chunk_loaded = vstipreset.fullchunk

#add reaper prog name or so
start = b'r\xa5\x00\x00\x01\x00\x00\x00'
vsti_chunk_combined = start + vsti_chunk_loaded

#split into size 210
length = 210
vsti_chunk_dec = [vsti_chunk_combined[i:i+length] for i in range(0, len(vsti_chunk_combined), length)]

#add reaper specific data for plugin
vsti_chunk_dec.insert(0, reaper_chunk_dec[0])
vsti_chunk_dec.insert(1, reaper_chunk_dec[1])
vsti_chunk_dec.insert(2, reaper_chunk_dec[2])
vsti_chunk_dec.append(reaper_chunk_dec[-1])

#compare reaper and vstpreset chunk before encoding
for a,b in zip(vsti_chunk_dec, reaper_chunk_dec):
    print(a==b)

#encode vstpreset chunk
vsti_chunk_raw = []
vsti_string_dec = bytes()
for ch in vsti_chunk_dec:
    vsti_string_dec += ch
    bt = base64.b64encode(ch).decode()
    vsti_chunk_raw.append(bt)

#compare reaper and vstpreset chunk after encoding
for a,b in zip(reaper_chunk_raw.vst_chunk, vsti_chunk_raw):
    print(a==b)

#set new chunk in reaper track
reaper_chunk_raw.vst_chunk= vsti_chunk_raw
rpre.load(reaper_chunk_raw)

print("Finished")