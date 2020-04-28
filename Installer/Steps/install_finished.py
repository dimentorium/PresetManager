from tkinter import *
from tkinter.ttk import *
from tkinter.constants import DISABLED, GROOVE, NORMAL
from tkinter import simpledialog, filedialog
import core.globals as glob
import os
import zipfile
from pathlib import Path
import configparser

class install_finished(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        header = Label(self, text="Install Python portable installation and Preset Manager for Reaper")
        header.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        Separator(self, orient="horizontal").grid(row=1, columnspan=4, padx=5, pady=5, sticky='ew')

        #configure label and button to select Reaper Folder
        self._lbl_reaper_folder = Label(self, text="""Installation finished. For any questions please visit:
        Reaper Forum: https://forum.cockos.com/showthread.php?p=2278667
        Github Repository: https://github.com/dimentorium/PresetManager""")
        self._lbl_reaper_folder.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)


    def perform_action(self):
        print("Finishing Installation")
        pass
