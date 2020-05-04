from tkinter.constants import TRUE
import reapy
from reapy.core import track
import os
import base64
import reaper.preset as rpre
import Converter.nksf as nksf

chunk = rpre.save()


base64_message = ''.join(chunk.vst_chunk[:])
message_bytes = base64.b64decode(base64_message)
#message = message_bytes.decode('utf-8')

msg = []
for ch in chunk.vst_chunk:
    bt = base64.b64decode(ch)
    msg.append(bt)
#msg[315].hex()
#vstipreset = vsti.VSTPreset("C:\\Users\\phili\\Desktop\\amped.vstpreset")

print("Test")

presetpath = "C:\\Users\\phili\\Downloads\\U-he - TyrellN6\\U-he - TyrellN6\\TyrellN6"
#presetpath = "C:\\Users\\phili\\Desktop\\NKS\\Omnisphere Library\\Bowed Color\\"

for filename in os.listdir(presetpath):
    preset_to_convert = nksf.NKSF(os.path.join(presetpath, filename), True, True, True)
    new_chunk = preset_to_convert._NKSF__chunks["PCHK"].data

    #split into size 280
    length = 210
    progchunk = [new_chunk[i:i+length] for i in range(0, len(new_chunk), length)]
    progchunk.insert(0, msg[0])
    progchunk.append(b'\x00')

    encoded_chunk = []
    for ch in progchunk:
        bt = base64.b64encode(ch).decode()
        encoded_chunk.append(bt)

    chunk.vst_chunk = encoded_chunk

    rpre.load(chunk)

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