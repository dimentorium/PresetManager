import os
import pickle
import core.globals as glob
import core.items as items

LIST_FOLDER = ""
LIST_FILE = ""
ITEMS = {}

def new(filepath:str):
    global ITEMS
    ITEMS = {}
    set_file_path(filepath)

def file_path() -> str:
    """File Path.

    Generating Filepath of database
    """
    global LIST_FOLDER
    global LIST_FILE
    return os.path.normpath(os.path.join(LIST_FOLDER, LIST_FILE))

def set_file_path(filepath:str):
    """Convert Filename.

    Generates filename and folder from absolute path
    """
    global LIST_FOLDER
    global LIST_FILE
    LIST_FOLDER, LIST_FILE = os.path.split(filepath)

    base, ext = os.path.splitext(LIST_FILE)
    if ext != ".bin":
        ext = ".bin"

    LIST_FILE = base + ext

def save():
    """Save database.

    Saves the complete database of presets into a binary file with pickle.
    User is asked for folder where to save
    """
    global ITEMS
    pickle.dump(ITEMS, open(file_path(), "wb"))

def load(filename):
    """Load database.

    Loads a database of presets from a binary file with pickle.
    User is asked for file where to load from
    """
    global ITEMS
    ITEMS = pickle.load(open(filename, "rb"))

def add(newitem):
    global ITEMS
    ITEMS[newitem.preset_name] = newitem

def get() -> dict:
    global ITEMS
    return ITEMS
