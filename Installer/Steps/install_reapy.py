from tkinter import *
from tkinter.ttk import *
from tkinter.constants import DISABLED, GROOVE, NORMAL
import core.globals as glob
import os
from pathlib import Path

class install_reapy(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        header = Label(self, text="Install REAPY API in Reaper")
        header.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        Separator(self, orient="horizontal").grid(row=1, columnspan=4, padx=5, pady=5, sticky='ew')

        #configure label and button to select Reaper Folder
        reapy_script_folder = glob.reaper_folder + "Python\\Reaper\\"
        self._lbl_reapy_script = Label(self, relief=GROOVE, text=reapy_script_folder)
        self._lbl_reapy_script.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        Separator(self, orient="horizontal").grid(row=3, columnspan=4, padx=5, pady=5, sticky='ew')

        #configure label and button to select Reaper ini
        self._lbl_reaper_info = Label(self, text="""Instruction for installing REAPY:
                                                    1. Start Reaper
                                                    2. Menu => Actions
                                                    3. Click "Show Actions List"
                                                    4. Click Button "Load" 
                                                    5. Open file from above
                                                    6. Click Button "Run"
                                                    7. Restart Reaper and click "Validate" Button
                                                    """)
        self._lbl_reaper_info.grid(row=4, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        self.btn_validate = Button(self,text="Validate REAPY", command=self.validate)
        self.btn_validate.grid(row=5, column=1, columnspan=3, sticky="nsew", padx=5, pady=5)

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

    def perform_action(self):
        #nothing to do from software
        print("Unzipping python")

    def validate(self):
        print("Validating REAPY")
        try:
            import reapy
            test = reapy.get_ini_file()
            if test != "":
                reapy.show_console_message("Validation successfull")
            else:
                messagebox.showerror('Failed', 'Could not validate REAPY')
        except:
            messagebox.showerror('Failed', 'Could not validate REAPY')
