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

item_tags = []

def get() -> list:
    """Init.

    Get the list of all tags

    Returns:
        item_tags: list of tags
    """
    global item_tags
    return item_tags

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
    global item_tags
    #read tags from file
    with open(tag_file()) as f:
        item_tags = f.read().splitlines()

def save():
    """Save.

    Saves taglist to file
    """
    global item_tags
    #read tags from file
    with open(tag_file(), 'w') as f:
        for listitem in item_tags:
            f.write('%s\n' % listitem)
