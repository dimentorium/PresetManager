# -*- coding: utf-8 -*-
"""Preset Manager Main.

Main startup to run the Prese Manager

Classes:
    controller: main classes handling the program and dataflow

Functions

Todo:
    * Better interface for loading and storing PResets
    * Load/Save multiple
    * Preview for NKSF
    * Load into empty track

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""
#============================================================#
#======================== Imports Section ====================#
import os
import logging
import queue

import openal
import pyogg

import core.globals as glob
import core.tags as tags
import core.ui as ui
import core.server as server


#============================================================#
#===========================Start Main Function==============#
def main():
    """Initialize Backend and start Preset Manager application."""
    #configure base file logger
    logging.basicConfig(filename='preset_manager.log',
                        level=logging.DEBUG, format='%(asctime)s %(message)s')

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)

    #start application
    logging.debug('Starting Preset manager main, V0.5.1, 11.06.2020')

    #set application folder
    glob.init(os.path.dirname(os.path.realpath(__file__)))
    logging.debug('Setting Application Path: %s', glob.application_folder)

    #read tags from file
    logging.debug('Loading tag file: %s', tags.tag_file())
    tags.load()
    logging.debug('Saving tag file: %s', tags.tag_file())
    tags.save()

    #Create command queue
    command_queue = queue.Queue()

    #start server
    server.start(command_queue)

    #start UI
    ui.start_main(command_queue)

#make sure to call main function
main()
