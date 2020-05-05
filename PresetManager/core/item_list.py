import logging
import os
import pickle
import core.globals as glob
import core.items as items

LIST_FOLDER = ""
LIST_FILE = ""
ITEMS = {}

def new(list_name, list_folder):
    global LIST_FOLDER
    LIST_FOLDER = list_folder
    global LIST_FILE
    LIST_FILE = list_name + ".bin"
    global ITEMS
    ITEMS = {}
    logging.debug("Item list created: " + LIST_FILE + " - " + LIST_FOLDER)

def file_path():
    """File Path.

    Generating Filepath of database
    """
    global LIST_FOLDER
    global LIST_FILE
    return os.path.join(LIST_FOLDER, LIST_FILE)

def convert_filename(filename):
    """Convert Filename.

    Generates filename and folder from absolute path
    """
    global LIST_FOLDER
    LIST_FOLDER = os.path.split(filename)[0]
    global LIST_FILE
    LIST_FILE = os.path.split(filename)[0]


def save():
    """Save database.

    Saves the complete database of presets into a binary file with pickle.
    User is asked for folder where to save
    """
    global ITEMS
    logging.debug('Saving Database: ' + file_path())
    pickle.dump(ITEMS, open(file_path(), "wb"))

def load(filename):
    """Load database.

    Loads a database of presets from a binary file with pickle.
    User is asked for file where to load from
    """
    global ITEMS
    #open file dialog to select database file and pickle data from file
    logging.debug('Loading Database: ' + filename)
    ITEMS = pickle.load(open(filename, "rb"))

def add(newitem):
    global ITEMS
    ITEMS[newitem.preset_name] = newitem
    logging.debug('Adding Preset: ' + newitem.preset_name)

def get() -> dict:
    global ITEMS
    return ITEMS
