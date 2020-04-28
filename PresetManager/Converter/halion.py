import reapy
from reapy.core import track
import rpp
import base64
import reaper.preset as rpre
import Converter.vstpreset as vsti

chunk = rpre.save("test")

msg = []
for ch in chunk.vst_chunk:
    bt = base64.b64decode(ch)
    msg.append(bt)

vstipreset = vsti.VSTPreset("C:\\Users\\phili\\Desktop\\Amped Mark 1.vstpreset")

print("Test")

fxpchunk = vstipreset.chunklist[0].data
fxpchunk = fxpchunk + vstipreset.chunklist[1].data

start = b'r\xa5\x00\x00\x01\x00\x00\x00'

combined = start + fxpchunk

#split into size 280
length = 210
progchunk = [combined[i:i+length] for i in range(0, len(combined), length)]
progchunk.insert(0, msg[0])
progchunk.insert(1, msg[1])
progchunk.insert(2, msg[2])
progchunk.append(msg[-1])

for a,b in zip(progchunk, msg):
    print(a==b)

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