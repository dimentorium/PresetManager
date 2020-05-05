# -*- coding: utf-8 -*-
"""VSTPreset module.

Handling of VSTPreset files with subclasses

Classes:
    Chunk: VSTPreset files contains chuns that are read and parsed
    VSTPreset: Main class for reading and parsing VSTPreset files

Todo:
    * save functionality

@author:         Philipp Noertersheuser
@GIT Repository: https://dev.azure.com/ainysynth/_git/ainysynth
@License
"""
import xmltodict
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

class VSTPreset(base.Preset):
    """VSTPreset class.

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

        vstpresetstream = open(filepath, "rb")
        self.__infodata = ""

        #read header information
        self.headerid = vstpresetstream.read(4).decode("utf-8")
        self.version = int.from_bytes(vstpresetstream.read(4), byteorder='little')
        self.classid = vstpresetstream.read(32).decode("utf-8")

        #read chunk offset, and position read
        offsettochunklist = int.from_bytes(vstpresetstream.read(8), byteorder='little')
        self.fullchunk = vstpresetstream.read()
        vstpresetstream.seek(offsettochunklist, 0)

        #Read list ID and number of entries
        self.listid = vstpresetstream.read(4).decode("utf-8")
        entrycount = int.from_bytes(vstpresetstream.read(4), byteorder='little')

        #empty chunklist and fileposition store
        self.chunklist = []
        filepos = 0
        for listentry in range(entrycount):
            #Read chunk
            currentchunk = Chunk()
            currentchunk.number = listentry
            currentchunk.id = vstpresetstream.read(4).decode("utf-8")
            currentchunk.offset = int.from_bytes(vstpresetstream.read(8), byteorder='little')
            currentchunk.size = int.from_bytes(vstpresetstream.read(8), byteorder='little')

            #store position as the list continues here
            filepos = vstpresetstream.tell()
            #position for chunk data, and read
            vstpresetstream.seek(currentchunk.offset, 0)
            currentchunk.data = vstpresetstream.read(currentchunk.size)

            #add chunk to list
            self.chunklist.append(currentchunk)

            #position cursor to read next chunk
            vstpresetstream.seek(filepos, 0)

        #Parse XML data from raw information
        for item in self.chunklist:
            if item.id == "Info":
                self.__parse_xml(item.data)
            elif item.id == "Comp":
                self.type = "Multi"
            elif item.id == "Prog":
                self.type = "Program"

    def __parse_xml(self, data):
        """Read XML data.

        Converts XML data and stores them in properties
        """
        self.__infodata = xmltodict.parse(data)
        self.tags = []
        #loop through items and search for attributes to use
        for item in self.__infodata['MetaInfo']['Attribute']:
            if item['@id'] == "MediaLibraryName":
                self.library = item['@value']
            elif item['@id'] == "MusicalCategory":
                self.category = item['@value']
                self.tags.append(self.category)
            elif item['@id'] == "MusicalCharacter":
                self.character = item['@value'].split("|")
                self.tags.extend(self.character)
            elif item['@id'] == "MusicalInstrument" :
                self.instrument = item['@value'].split("|")
                self.tags.extend(self.instrument)
            elif item['@id'] == "MusicalStyle" :
                self.style = item['@value']
                self.tags.extend(self.style)
            elif item['@id'] == "MusicalSubStyle" :
                self.instrument = item['@value'].split("|")
                self.tags.extend(self.substyle)
            elif item['@id'] == "PlugInName":
                self.pluginname = item['@value']
