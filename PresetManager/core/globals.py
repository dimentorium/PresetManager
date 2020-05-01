import os


root = None
application_folder = ""
database_folder = ""
database_name = ""
main_window = None

def tag_file():
    return os.path.join(application_folder, "item_tags.txt")

def render_file():
    return os.path.join(application_folder, "renderproject.rpp")
