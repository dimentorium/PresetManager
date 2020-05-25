import os
import re
from typing import List
import reapy

__VST_LIST = []

class vst_plugin:
    """VST Plugin Class

    Class containing different values from the ini file for each plugin
    """
    dll_name = ""
    reaper_id = ""
    vst_id = ""
    reaper_name = ""

    def lookup(self, lookup_string:str) -> bool:
        """Lookup VST Plugin.

        Test if the lookup string matches the given plugin

        Arguments:
            lookup_string {str} -- Lookup string to compare

        Returns:
            bool -- True if lookup string matches plugin
        """
        match = False

        if lookup_string.lower() == self.dll_name.lower():
            match = True
        elif lookup_string.lower() == self.vst_id.lower():
            match = True
        elif lookup_string.lower() == self.reaper_name.lower():
            match = True
        elif lookup_string.lower() in self.reaper_name.lower():
            match = True
        elif lookup_string.lower() == os.path.splitext(self.dll_name)[0].lower():
            match = True
        
        return match
        

def load():
    """Load vst plugins file.

    searches and loads the file in Reaper that contains
    information on all registered VSTs. 
    """
    global __VST_LIST

    #get path to ini file containing vst plugins
    ini_folder = os.path.split(reapy.get_ini_file())[0]
    plugin_ini = os.path.join(ini_folder, "reaper-vstplugins64.ini")

    #read lines from file
    with open(plugin_ini) as f:
        content = f.readlines()

    #split lines into information
    for vst in content[1:]:
        splitted_line = re.split("=|,", vst)

        #currently only VST2 plugins are supported
        if splitted_line[0].endswith(".dll"):
            vst_to_add = vst_plugin()
            vst_to_add.dll_name = splitted_line[0]
            vst_to_add.reaper_id = splitted_line[1]

            if len(splitted_line) >= 3:
                hex_value = hex(int(splitted_line[2]))
                hex_string = hex_value[2:]
                bytes_object = bytes.fromhex(hex_string)
                vst_to_add.vst_id = bytes_object.decode()

            if len(splitted_line) >= 4:
                vst_to_add.reaper_name = splitted_line[3].split("(")[0].lstrip().rstrip()

            __VST_LIST.append(vst_to_add)

def lookup(lookup_string: str):
    """Looukp for plugin

    Function uses the given string to find appropriate plugin that matches
    the search.

    Arguments:
        lookup_string {str} -- string that should be searched for, can be name, dll or ID

    Returns:
        bool -- True if element found
        vst_plugin -- information about plugin that matches lookup
    """
    global __VST_LIST

    for vst in __VST_LIST:
        if vst.lookup(lookup_string):
            return True, vst
    
    return False, vst_plugin()


load()