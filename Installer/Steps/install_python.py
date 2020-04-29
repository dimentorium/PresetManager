from tkinter import *
from tkinter.ttk import *
from tkinter.constants import DISABLED, GROOVE, NORMAL
from tkinter import simpledialog, filedialog
import core.globals as glob
import os
import zipfile
from pathlib import Path
import configparser
import logging

class install_python(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        logging.debug("Starting Step: Install Python")
        self._selected_folder = ""
        self._installation_type = ""
        self._ini_file = ""

        header = Label(self, text="Install Python portable installation to Reaper")
        header.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        Separator(self, orient="horizontal").grid(row=1, columnspan=4, padx=5, pady=5, sticky='ew')

        #configure label and button to select Reaper Folder
        self._lbl_reaper_folder = Label(self, relief=GROOVE)
        self._lbl_reaper_folder.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        self.btn_folder = Button(self,text="Select Folder", command=self.select_folder)
        self.btn_folder.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        Separator(self, orient="horizontal").grid(row=3, columnspan=4, padx=5, pady=5, sticky='ew')

        #configure label and button to select Reaper ini
        self._lbl_reaper_info = Label(self, text="Installation Information")
        self._lbl_reaper_info.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        self._lbl_reaper_ini = Label(self, relief=GROOVE)
        self._lbl_reaper_ini.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)
        self._lbl_reaper_install = Label(self)
        self._lbl_reaper_install.grid(row=5, column=1, sticky="nsew", padx=5, pady=5)

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

    def select_folder(self):
        """Select Folder.

        Open Dialog to select folder for database
        """
        self._selected_folder = filedialog.askdirectory(title="Select folder")
        if self._selected_folder != "":
            logging.debug("Selected Reaper Folder: " + self._selected_folder)
            glob.reaper_folder = self._selected_folder
            self._lbl_reaper_folder['text'] = self._selected_folder
            self.check_ini()


    def perform_action(self):
        
        installation_folder = self._lbl_reaper_folder['text'] + "\\Python"
        installation_folder = installation_folder.replace("/","\\")
        logging.debug("Unzipping python to: " + installation_folder)
        with zipfile.ZipFile(glob.python_zip, 'r') as zip_ref:
            zip_ref.extractall(installation_folder)

        #set keys in Reaper.ini file and write config
        logging.debug("Setting keys in: " + self._ini_file)
        Config = configparser.ConfigParser()
        Config.read(self._ini_file)
        Config.set("REAPER", "pythonlibpath64", installation_folder)
        Config.set("REAPER", "pythonlibdll64", "python37.dll")
        Config.set("REAPER", "reascript", "1")

        with open(self._ini_file, 'w') as configfile:
            Config.write(configfile)

    def check_ini(self):
        if os.path.isfile(str(Path.home()) + "\\AppData\\Roaming\\REAPER\\reaper.ini"):
            logging.debug ("Normal installation found:" + self._selected_folder)
            self._lbl_reaper_ini["text"] = str(Path.home()) + "\\AppData\\Roaming\\REAPER\\reaper.ini"
            self._lbl_reaper_install["text"] = "Normal Installation"
            self._ini_file = str(Path.home()) + "\\AppData\\Roaming\\REAPER\\reaper.ini"
            
        elif os.path.isfile(self._selected_folder + "\\reaper.ini"):
            logging.debug ("Portable installation found:" + self._selected_folder)
            self._lbl_reaper_ini["text"] = self._selected_folder + "\\reaper.ini"
            self._lbl_reaper_install["text"] = "Portable Installation"
            self._ini_file = self._selected_folder + "\\reaper.ini"

        if self._ini_file != "":
            Config = configparser.ConfigParser()
            Config.read(self._ini_file)
            ppath = Config.has_option("reaper", "pythonlibpath64")
            plib = Config.has_option("reaper", "pythonlibdll64")
            if ppath and plib:
                logging.debug("Found Python Configuration")
