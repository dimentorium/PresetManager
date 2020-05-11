# -*- coding: utf-8 -*-
"""Preset Manager Main.

Main startup to run the Prese Manager

Classes:
    controller: main classes handling the program and dataflow

Functions

Todo:
    * Refactoring to hve cleaner structure

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""
#============================================================#
#======================== Imorts Section ====================#
import os
import logging
import core.globals as glob
import core.tags as tags
import core.ui as ui
import reaper.server as server

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
    logging.debug('Starting Preset manager main, V0.0.3, 11.05.2020')

    #set application folder
    glob.application_folder = os.path.dirname(os.path.realpath(__file__))
    logging.debug('Setting Application Path: %s', glob.application_folder)

    #read tags from file
    logging.debug('Loading tag file: %s', tags.tag_file())
    tags.load()
    logging.debug('Saving tag file: %s', tags.tag_file())
    tags.save()

    #start server
    server.start()

    #start UI
    ui.start_main()

#make sure to call main function
main()
