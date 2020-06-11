# -*- coding: utf-8 -*-
"""Item List module.

Module for handling the list of all items. Is used as a singleton

Functions
initialized: Shows if database has been initialized and ca be used

Todo:

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""

import os
import pickle
import core.globals as glob
import core.items as items

__DATABASE_FILE = ""
__ITEMS = {}
__INITIALIZED = False

def initialized() -> bool:
    """Check if database is initialized.

    Reads variable to make sure the database can be used and accessed
    """
    return __INITIALIZED

def new(filepath: str):
    """Create New Database.

    Creates new empty database
    """
    global __ITEMS
    __ITEMS = {}
    set_file_path(filepath)
    global __INITIALIZED
    __INITIALIZED = True
    save()

def file_path() -> str:
    """File Path.

    Returns filepath of database
    """
    global __DATABASE_FILE
    return __DATABASE_FILE

def set_file_path(filepath: str):
    """Set Database File Path.

    Checks file path and ending and stores it
    """
    global __DATABASE_FILE
    db_folder, db_file = os.path.split(filepath)

    #check if file ends on .bin otherwise replace this
    base, ext = os.path.splitext(db_file)
    if ext != ".bin":
        ext = ".bin"

    __DATABASE_FILE = os.path.normpath(os.path.join(db_folder, base + ext))

def folder_name() -> str:
    """Return folder.

    Returns the folderpath where the database is located
    """
    global __DATABASE_FILE
    return os.path.split(__DATABASE_FILE)[0]

def file_name() -> str:
    """Return filename.

    Returns the filenam of the database
    """
    global __DATABASE_FILE
    return os.path.split(__DATABASE_FILE)[1]

def save():
    """Save database.

    Saves the complete database of presets into a binary file with pickle.
    """
    global __ITEMS
    pickle.dump(__ITEMS, open(file_path(), "wb"))

def load(filename):
    """Load database.

    Loads a database of presets from a binary file with pickle.
    User is asked for file where to load from
    """
    set_file_path(filename)
    global __ITEMS
    __ITEMS = pickle.load(open(filename, "rb"))
    global __INITIALIZED
    __INITIALIZED = True

def add(newitem):
    """Add item.

    Adds an itme to the list
    """
    global __ITEMS
    __ITEMS[newitem.preset_name] = newitem

def update(newitem):
    """Update item.

    Updates an item in the list
    """
    global __ITEMS
    __ITEMS[newitem.preset_name] = newitem

def get(search_filter: str, tags: list) -> dict:
    """Get all items.

    returns full list of items
    """
    global __ITEMS
    items_with_tags = {}
    
    #select only items that have selected tags
    if len(tags) > 0:
        for key, value in __ITEMS.items():
            if all(tag in value.search_tags() for tag in tags):
                items_with_tags[key] = value
    else:
        items_with_tags = __ITEMS

    #select only items with appropriate filters
    items_to_return = {}
    if search_filter != "":
    #loop over all items in list
        for key, value in items_with_tags.items():
            #call filter function from item to check if it should be shown
            show = value.check_filter(search_filter)

            #show item based on filter function result
            if show:
                items_to_return[key] = value
    else:
        items_to_return = items_with_tags

    return items_to_return