import os

def set_application_folder(folder: str):
    global application_folder
    application_folder = folder

    global data_folder
    data_folder = os.path.join(application_folder, "data")

    global pm_zip
    pm_zip = os.path.join(data_folder, "PresetManager.zip")

    global python_zip
    python_zip = os.path.join(data_folder, "python_reaper.zip")

root = None
application_folder = ""
data_folder = ""
pm_zip = ""
python_zip = ""


reaper_folder = ""
pm_folder = ""


