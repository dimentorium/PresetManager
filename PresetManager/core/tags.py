# -*- coding: utf-8 -*-
"""Tags.

Module for handling tags that are used to classify items

Variables:
    __ITEM_TAGS: internal list of all tags

Functions:
    get: Gets list of tags
    tag_file: file path of tag file
    load: Loads tags from file
    save: Save tags to file

Todo:

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""
import core.globals as glob
import os

__ITEM_TAGS = []

def get() -> list:
    """Init.

    Get the list of all tags

    Returns:
        item_tags: list of tags
    """
    global __ITEM_TAGS
    return __ITEM_TAGS

def tag_file() -> str:
    """Tag File.

    Returns absolute path to tag file

    Returns:
        filepath: absolute path to tag file
    """
    return os.path.join(glob.data_folder, "item_tags.txt")

def load():
    """Load.

    Loads taglist from file
    """
    global __ITEM_TAGS
    #read tags from file
    if os.path.exists(tag_file()):
        with open(tag_file()) as file_to_read:
            __ITEM_TAGS = file_to_read.read().splitlines()
    else:
        #no tag file existing, create new
        __ITEM_TAGS = []
        save()

def save():
    """Save.

    Saves taglist to file
    """
    global __ITEM_TAGS
    #read tags from file
    with open(tag_file(), 'w') as file_to_write:
        for listitem in __ITEM_TAGS:
            file_to_write.write('%s\n' % listitem)

def update(tag_list: list):
    """Update Tag List.

    Checks if new tags are already in list and adds these if not
    """
    global __ITEM_TAGS
    for tag in tag_list: 
        if tag not in __ITEM_TAGS: 
            __ITEM_TAGS.append(tag) 

