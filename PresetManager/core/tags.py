# -*- coding: utf-8 -*-
"""Tags.

Module for handling tags that are used to classify items

Variables:
    item_tags: internal list of all tags

Functions:
    get: Gets list of tags
    tag_file: file path of tag file
    load: Loads tags from file
    save: Save tags to file

Todo:
    * Refactoring to hve cleaner structure

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""
import core.globals as glob
import os
import logging

ITEM_TAGS = []

def get() -> list:
    """Init.

    Get the list of all tags

    Returns:
        item_tags: list of tags
    """
    global ITEM_TAGS
    return ITEM_TAGS

def tag_file():
    """Tag File.

    Create filepath 

    Returns:
        filepath: absolute path to tag file
    """
    return os.path.join(glob.application_folder, "item_tags.txt")

def load():
    """Load.

    Loads taglist from file
    """
    global ITEM_TAGS
    #read tags from file
    logging.debug('Loading tag file: ' + tag_file())
    with open(tag_file()) as f:
        ITEM_TAGS = f.read().splitlines()

def save():
    """Save.

    Saves taglist to file
    """
    global ITEM_TAGS
    #read tags from file
    logging.debug('Saving tag file: ' + tag_file())
    with open(tag_file(), 'w') as f:
        for listitem in ITEM_TAGS:
            f.write('%s\n' % listitem)
