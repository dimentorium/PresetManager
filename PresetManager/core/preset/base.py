# -*- coding: utf-8 -*-
"""Base module.

Abstract class for deriving other preset files

Classes:
    preset: abstract class

Todo:
    *

@author:         Philipp Noertersheuser
@GIT Repository: https://dev.azure.com/ainysynth/_git/ainysynth
@License
"""
import os

class Preset:
    """
    Base class for presets.

    Base class for presets where all others should be derived from
    This is an abstract class that does not contain any functionality

    Attributes
    ----------
        filepath: absolute path to preset file
        name: name of preset
        filetype: ending of preset file
        library: name of library
        tags: tags extracted from preset file
        instrument: list of instrument tags
        character: list of character tags
        category: string for category
        style: list of style tags
        substyle: list of substyle tags

    Methods
    -------
        init: inititalizes class
    """

    def __init__(self, filepath: str):
        """Init class.

        Initializes class with empty values or information from the filepath

        Parameters
        ----------
        filepath: absolute path to file

        """
        self.__filepath = filepath
        filename = os.path.basename(self.__filepath)
        self.name = filename.split(".")[0]
        self.filetype = filename.split(".")[1]
        self.library = ""
        self.pluginname = ""
        self.tags = []
        self.instrument = []
        self.character = []
        self.category = []
        self.style = []
        self.substyle = []
