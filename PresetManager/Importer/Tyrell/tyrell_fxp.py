import reapy
from reapy.core import track
import rpp
import base64
import reaper.preset as rpre
import Converter.fxp as fxp

#load chunk from reaper and decode it
chunk_from_reaper = rpre.save()
decoded_chunk_from_reaper = chunk_from_reaper.decode_vst_chunk()


#load fxp preset file
#filepath= "C:\\Users\\phili\\Desktop\\Tyrell_bbb.FXP"
filepath = r"C:\Users\phili\Desktop\Pianoteq_custom2.FXP"
fxppreset = fxp.FXPPreset(filepath)

#start stuff og pianoteq b'\xa0\x98\x13\xfe\x02\x00\x00\x00H8\x12\x00r\x17\x0b\x00 \x00\x00\x00\x118V8\xf9V\x01\x00
start = b'\xa0\x98\x13\xfe\x02\x00\x00\x00H8\x12\x00r\x17\x0b\x00 \x00\x00\x00\x118V8\xf9V\x01\x00'
combined = start + fxppreset.fxpchunk
#combined = fxppreset.fxpchunk

#split into size 280
length = 210
progchunk = [combined[i:i+length] for i in range(0, len(combined), length)]

#header from reaper, Tyrell = 0, Halion = 0,1,2
progchunk.insert(0, decoded_chunk_from_reaper[0])

progchunk.append(b'\x00')
msg2 = []
for ch in progchunk:
    bt = base64.b64encode(ch).decode()
    msg2.append(bt)

#for a,b in zip(chunk.vst_chunk, msg2):
#    print(a==b)

chunk_from_reaper.vst_chunk= msg2

rpre.load(chunk_from_reaper)

chunktest = rpre.save()

print("Test")




"""
The VST Chunk is stored as base64 in the track chunk. I assume if you look at the track chunk you'll have to decode it manually... The format of the binary blob (once decoded from base64) is like this:

4 bytes <VSTID>
4 bytes <magic value?>
4 bytes <Number of Inputs>
* after that, a bitmask array of 8 bytes each, for the input routings (bit 0 = input channel 1 is set; bit 63 = input channel 64 is set; etc)
* the length of the above array is defined by the number of inputs (so total size is 8*NumInputs bytes)

4 bytes <Number of Outputs>
* again bitmask array 8 bytes each for outputs this time... 
"""