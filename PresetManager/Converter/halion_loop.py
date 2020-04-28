import os
import Converter.vstpreset as vsti
import reapy
import pickle
import reaper.preset as rp
import core.items as items
import time
import sys

multi_folder = "C:\\Users\\phili\\Desktop\\Halion\\Multi"
program_folder = "C:\\Users\\phili\\Desktop\\Halion\\Program"
dbfile = "C:\\Users\\phili\\Desktop\\Halion\\halion.bin"

project = reapy.Project()
selected_track = project.get_selected_track(0)

preset_list = {}
filelist = os.listdir(multi_folder)

count = 0
overall = 0
for file in filelist:
    try:
        print("Loading: " + str(overall) + " of " + str(len(filelist)) + "|" + file)
        filename = file.split(".")[0]
        multi_preset = vsti.VSTPreset(os.path.join(multi_folder, file))
        program_preset = vsti.VSTPreset(os.path.join(program_folder, file))

        selected_track.fxs[0].preset = os.path.join(multi_folder, file)
        time.sleep(2)

        #get chunk from selected track
        newpreset = rp.save(filename)
        #create new item and add it to database
        vsti_item = items.vstipreset(filename, newpreset, program_preset.tags)
        preset_list[filename] = vsti_item
        count += 1
        overall += 1
        if count > 100:
            pickle.dump(preset_list, open(dbfile,"wb"))
            count = 0

    except Exception as e:
        e = sys.exc_info()[0]
        print("An exception occurred: " + str(e)) 


pickle.dump(preset_list, open(dbfile,"wb"))