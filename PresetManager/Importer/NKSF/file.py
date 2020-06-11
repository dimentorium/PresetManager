# -*- coding: utf-8 -*-
"""NKSF module.

Handling of NKSF files with subclasses

Classes:
    Riffchunk: NKSF files contain riffchunks that are read and parsed
    NKSF: Main class for handling NKSF files

Todo:
    * save functionality
    * issues with reading chunks

@author:         Philipp Noertersheuser
@GIT Repository: https://dev.azure.com/ainysynth/_git/ainysynth
@License
"""
import io
import os
import msgpack
import collections
from typing import Dict, List
import reaper.preset as rp

class RiffChunk:
    """Riffchunk Class.

    Class containing properties to hold riffchunk data

    Attributes
    ----------
        id: string identifier for chunk, 4 bytes
        size: raw data size in bytes, 4 bytes
        version: optional 4 byte identifier
        data: raw byte data
        info: data decoded with msgpack

    Methods
    -------
        init: resets all attributes
    """

    def __init__(self):
        """Init class.

        Initialize class properties.
        """
        self.id = 0
        self.size = 0
        self.version = 0
        self.data = ""
        self.info = ""

class NKSF_file():
    """NKSF Preset class.

    Class containing chunks and wrapper properties

    Methods
    -------
        init: resets all attributes
        msg_to_tuple: convert data in riffchunk with messagepack parser
        GetLibraryName: get name of library
        GetTags: Get Tags from library

    """

    def __init__(self, filepath: str, parse_NICA = False, parse_PLID = False, parse_PCHK = False):
        """Init class.

        Initialize class properties.

        Parameters
        ----------
            filepath: absolute path of NKS file to be loaded
            parse_NICA: parse Controller assignment
            parse_PLID: parse Plugin ID 
            parse_PCHK: parse Plugin Chunk
        """
        self.__filepath = filepath
        filename = os.path.basename(self.__filepath)
        self.preset_name = filename.split(".")[0]
        self.filetype = filename.split(".")[1]
        self.library = ""
        self.plugin_name = ""
        self.type = "NKSF Preset"
        self.tags = []
        self.instrument = []
        self.character = []
        self.category = []
        self.style = []
        self.substyle = []

        nkfsstream = open(filepath, "rb")
        self.__chunks = {}

        #read header information and add to chunklist
        header = RiffChunk()
        header.id = nkfsstream.read(4)
        header.size = int.from_bytes(nkfsstream.read(4), byteorder='little')
        header.data = nkfsstream.read(4)
        self.__chunks["header"] = header

        #Read Summary Information 
        NISI = RiffChunk()
        NISI.id = nkfsstream.read(4)
        NISI.size = int.from_bytes(nkfsstream.read(4), byteorder='little')
        NISI.version = int.from_bytes(nkfsstream.read(4), byteorder='little')
        NISI.data = nkfsstream.read(self._calc_data_size(NISI.size-4))
        NISI.info = self.__msg_to_tuple(NISI.data[:NISI.size-4])
        self.__chunks["NISI"] = NISI

        #Read Controller Assignment
        if parse_NICA:
            NICA = RiffChunk()
            NICA.id = nkfsstream.read(4)
            NICA.size = int.from_bytes(nkfsstream.read(4), byteorder='little')
            NICA.version = int.from_bytes(nkfsstream.read(4), byteorder='little')
            NICA.data = nkfsstream.read(self._calc_data_size(NICA.size-4))
            NICA.info = self.__msg_to_tuple(NICA.data)
            self.__chunks["NICA"] = NICA

        #Read Plugin ID
        if parse_PLID:
            PLID = RiffChunk()
            PLID.id = nkfsstream.read(4)
            PLID.size = int.from_bytes(nkfsstream.read(4), byteorder='little')
            PLID.version = int.from_bytes(nkfsstream.read(4), byteorder='little')
            PLID.data = nkfsstream.read(self._calc_data_size(PLID.size-4))
            self.__chunks["PLID"] = PLID

        #Read Plugin Chunk
        if parse_PCHK:
            PCHK = RiffChunk()
            PCHK.id = nkfsstream.read(4)
            PCHK.size = int.from_bytes(nkfsstream.read(4), byteorder='little')
            PCHK.version = int.from_bytes(nkfsstream.read(4), byteorder='little')
            PCHK.data = nkfsstream.read(self._calc_data_size(PCHK.size-4))
            self.__chunks["PCHK"] = PCHK

        if NISI.info != "":
            for key, value in NISI.info.items():
                if key == "bankchain":
                    self.library = value[1:]
                    self.plugin_name = value[0]
                elif key == "characters":
                    self.character = value
                elif key == "modes":
                    self.category = value
                elif key == "types":
                    self.tags = self.__convert_to_list(value, [])
                else:
                    pass

        """
        self.style = []
        self.substyle = []
        """

    def load(self) -> bool:
        rp.load_vst_chunk(self.plugin_name,self.__chunks["PCHK"].data)
        return True

    @property
    def properties(self) -> Dict:
        return_dict = {}
        return_dict["DAW"] = "Any"
        return return_dict

    def search_tags(self) -> List:
        return ["NKSF Instrument"]

    #todo: function for flattening the data
    def __convert_to_list(self, values, final_list=[]):
        for value in values:
            if type(value) is str:
                final_list.append(value)
            elif type(value) is list:
                if len(value) == 1:
                    final_list.append(value[0])
                elif len(value) == 2:
                    final_list.append(value[0] + "+" + value[1])
                else:
                    self.__convert_to_list(value, final_list)

        return final_list

    def _calc_data_size(self, size):
        #a pad byte, if the chunk's length is not even.
        final_size = size
        if (size % 2) == 1:
            final_size = size + 1
        return final_size

    def __msg_to_tuple(self, data: str) -> str:
        """Convert Messagepack.

        Converts raw byte data with msgpack to python tuples for better accessing

        Parameters
        ----------
            data: raw byte data

        Returns
        -------
            tuple: decoded and parsed data with id and value
        """
        parsed = ""
        try:
            unp = io.BytesIO(data)
            parsed = msgpack.unpack(unp, raw=False)
        except:
            parsed = ""
        return parsed