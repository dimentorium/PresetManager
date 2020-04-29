from tkinter import *
from tkinter.ttk import *
from tkinter.constants import DISABLED, GROOVE, NORMAL
from tkinter import filedialog
import core.globals as glob
import zipfile
import logging

class install_presetmanager(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        logging.debug("Starting Step: Install Presetmanager")

        self._selected_folder = ""
        self._installation_type = ""
        self._ini_file = ""

        header = Label(self, text="Please select folder where to install Preset Manager")
        header.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        Separator(self, orient="horizontal").grid(row=1, columnspan=4, padx=5, pady=5, sticky='ew')

        #configure label and button to select Reaper Folder
        self._lbl_pm_folder = Label(self, relief=GROOVE)
        self._lbl_pm_folder.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        self.btn_folder = Button(self,text="Select Folder", command=self.select_folder)
        self.btn_folder.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        Separator(self, orient="horizontal").grid(row=3, columnspan=4, padx=5, pady=5, sticky='ew')

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

    def select_folder(self):
        """Select Folder.

        Open Dialog to select folder for database
        """
        self._selected_folder = filedialog.askdirectory(title="Select folder")
        if self._selected_folder != "":
            logging.debug("Setting PM Installation folder: " + self._selected_folder)
            glob.pm_folder = self._selected_folder
            self._lbl_pm_folder['text'] = self._selected_folder


    def perform_action(self):
        logging.debug("Unzipping Preset Manager")
        installation_folder = self._lbl_pm_folder['text'] + "\\PresetManager"
        installation_folder = installation_folder.replace("/","\\")
        with zipfile.ZipFile(glob.pm_zip, 'r') as zip_ref:
            zip_ref.extractall(installation_folder)
