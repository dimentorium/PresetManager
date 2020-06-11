
import reapy
from reapy.core import track
import rpp
import base64
import reaper.preset as rpre

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
#filepath= "C:\\Users\\phili\\Desktop\\bbb.FXP"
filepath = "C:\\Tyrell\\TyrellN6.data\\Presets\\TyrellN6\\Chapter 3.h2p"
fxppresetstream = open(filepath, "rb")
fxpchunk = fxppresetstream.read()
fxpchunk = fxpchunk.replace(b"\\r", b"\r")
fxpchunk = fxpchunk.replace(b"\\n", b"\n")
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
    print(a == b)

chunk.vst_chunk = msg2

rpre.load(chunk)