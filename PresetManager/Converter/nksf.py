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
import msgpack
import converter.base as base

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

class NKSF(base.Preset):
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
        super().__init__(filepath)
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
        NISI.data = nkfsstream.read(NISI.size-4)
        NISI.info = self.__msg_to_tuple(NISI.data)
        self.__chunks["NISI"] = NISI

        #Read Controller Assignment
        if parse_NICA:
            NICA = RiffChunk()
            NICA.id = nkfsstream.read(4)
            NICA.size = int.from_bytes(nkfsstream.read(4), byteorder='little')
            NICA.version = int.from_bytes(nkfsstream.read(4), byteorder='little')
            if NICA.size-4 > 0:
                NICA.data = nkfsstream.read(NICA.size-4)
            else:
                NICA.data = ""
                NICA.info = self.__msg_to_tuple(NICA.data)
                self.__chunks["NICA"] = NICA

        #Read Plugin ID
        if parse_PLID:
            PLID = RiffChunk()
            PLID.id = nkfsstream.read(4)
            PLID.size = int.from_bytes(nkfsstream.read(4), byteorder='little')
            PLID.version = int.from_bytes(nkfsstream.read(4), byteorder='little')
            PLID.data = nkfsstream.read(PLID.size-4)
            self.__chunks["PLID"] = PLID

        #Read Plugin Chunk
        if parse_PCHK:
            PCHK = RiffChunk()
            PCHK.id = nkfsstream.read(4)
            PCHK.size = int.from_bytes(nkfsstream.read(4), byteorder='little')
            PCHK.data = nkfsstream.read(PCHK.size)
            self.__chunks["PCHK"] = PCHK

        """not yet stable
        self.library = self.__chunks["NISI"].info["bankchain"][1:]
        self.pluginname = self.__chunks["NISI"].info["bankchain"][0]
        self.tags = []
        self.instrument = []
        self.character = self.__chunks["NISI"].info["characters"]
        self.category = self.__chunks["NISI"].info["modes"]
        self.style = []
        self.substyle = []
        self.tags = self.__chunks["NISI"].info["types"]
        """

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