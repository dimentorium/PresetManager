import reapy
from reapy.core import track
import rpp
import base64
import reaper.preset as rpre
import Converter.vstpreset as vsti

chunk = rpre.save("test")


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


start = "#pgm=bbb Funkeee\n"
filepath= "C:\\Users\\phili\\Desktop\\bbb.FXP"
fxppresetstream = open(filepath, "rb")
chunkmagic = fxppresetstream.read(4).decode("utf-8")
size = int.from_bytes(fxppresetstream.read(4), byteorder='big')
fxmagic = fxppresetstream.read(4).decode("utf-8")
version = int.from_bytes(fxppresetstream.read(4), byteorder='big')
fxid = int.from_bytes(fxppresetstream.read(4), byteorder='big')
fxversion = int.from_bytes(fxppresetstream.read(4), byteorder='big')
numparams = int.from_bytes(fxppresetstream.read(4), byteorder='big')
prgname = fxppresetstream.read(28).decode("utf-8")
chunksize = int.from_bytes(fxppresetstream.read(4), byteorder='big')
fxpchunk = fxppresetstream.read()

combined = start.encode() + fxpchunk

#split into size 280
length = 210
progchunk = [combined[i:i+length] for i in range(0, len(combined), length)]
progchunk.insert(0, msg[0])

progchunk.append(b'\x00')
msg2 = []
for ch in progchunk:
    bt = base64.b64encode(ch).decode()
    msg2.append(bt)

for a,b in zip(chunk.vst_chunk, msg2):
    print(a==b)

chunk.vst_chunk= msg2

rpre.load(chunk)

chunktest = rpre.save("test")

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