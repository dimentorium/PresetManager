# -*- coding: utf-8 -*-
"""FXPPreset module.

Handling of FXPPreset files with subclasses

Classes:
    Chunk: VSTPreset files contains chuns that are read and parsed
    VSTPreset: Main class for reading and parsing VSTPreset files

Todo:
    * save functionality

@author:         Philipp Noertersheuser
@GIT Repository: https://dev.azure.com/ainysynth/_git/ainysynth
@License
"""
import core.preset.base as base

class Chunk:
    """Chunk Class.

    Class containing properties to hold chunk data

    Attributes
    ----------
        id: string identifier for chunk, 4 bytes
        offset: chunk start byte from file start
        size: raw data size in bytes, 4 bytes
        data: raw byte data
        number: index in list

    Methods
    -------
        init: resets all attributes

    """

    def __init__(self):
        """Init class.

        Initialize class properties.
        """
        self.id = 0
        self.offset = 0
        self.size = 0
        self.data = ""
        self.number = 0

class FXPPreset(base.Preset):
    """FXPPreset class.

    Class containing chunks and wrapper properties

    Attributes
    ----------
        infodata: converted XML chunk
        headerid: id for VSTPreset file
        version: version number
        classid: numeric identifier for class
        chunklist: raw chunks read from file

    Methods
    -------
        init: resets all attributes
        parse_xml: read information from XML chunk

    """

    def __init__(self, filepath: str):
        """Init class.

        Initialize class properties from absolute filepath

        Parameters
        ----------
            filepath: absolute path of NKS file to be loaded

        """
        #load file
        super().__init__(filepath)

        #read filestream
        fxppresetstream = open(filepath, "rb")

        #read chunkmagic, should be CcnK
        self.chunkmagic = fxppresetstream.read(4).decode("utf-8")

        #complete size of chunk withou chunkmagic and bytesize
        self.size = int.from_bytes(fxppresetstream.read(4), byteorder='big')

        #FxCk for parameters, FPCh for chunk
        self.fxmagic = fxppresetstream.read(4).decode("utf-8")

        #Version of Preset
        self.version = int.from_bytes(fxppresetstream.read(4), byteorder='big')

        #ID of FX, 4 Letters and Version of FX
        self.fxid = fxppresetstream.read(4).decode("utf-8")
        self.fxversion = int.from_bytes(fxppresetstream.read(4), byteorder='big')

        #Number of Parameters
        self.numparams = int.from_bytes(fxppresetstream.read(4), byteorder='big')

        #Name of Prgram max 28 bytes zero terminated
        self.prgname = fxppresetstream.read(28).decode("utf-8")

        #size of chunk for preset and raw chunk data
        self.chunksize = int.from_bytes(fxppresetstream.read(4), byteorder='big')
        self.fxpchunk = fxppresetstream.read()