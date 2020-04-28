from tkinter import *
from tkinter.ttk import *
from tkinter.constants import DISABLED, GROOVE, NORMAL
from tkinter import simpledialog, filedialog
import core.globals as glob
import os
import zipfile
from Steps.install_python import install_python
from Steps.install_reapy import install_reapy
from Steps.install_welcome import install_welcome
from Steps.install_presetmanager import install_presetmanager
from Steps.install_finished import install_finished

class Wizard():
    def __init__(self):
        self.root = Tk()
        self.root.title("Preset Manager Installer")

        self.current_step = None
        
        self.content_frame = Frame(self.root, relief=GROOVE, padding=5)
        self.content_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.button_frame = Frame(self.root, padding=5)
        self.back_button = Button(self.button_frame, text="<< Back", command=self.back)
        self.back_button.pack(side=LEFT, padx=5, pady=5)
        self.next_button = Button(self.button_frame, text="Next >>", command=self.next)
        self.next_button.pack(side=LEFT, padx=5, pady=5)
        self.finish_button = Button(self.button_frame, text="Finish", command=self.finish)
        self.finish_button.pack(side=LEFT, padx=5, pady=5)
        self.button_frame.grid(row=1, column=1, sticky="se")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.steps = [install_welcome, install_python, install_reapy, install_presetmanager, install_finished]
        self.show_step(0)

        # Gets the requested values of the height and widht.
        windowWidth = 640
        windowHeight = 480
        self.root.minsize(windowWidth, 480)
        print("Width",windowWidth,"Height",windowHeight)
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.root.winfo_screenheight()/2 - windowHeight/2)
        # Positions the window in the center of the page.
        self.root.geometry("+{}+{}".format(positionRight, positionDown))

        self.root.mainloop()

    def show_step(self, step):
        if self.current_step is not None:
            # remove current step
            self.current_step.pack_forget()

        self.step_no = step
        self.current_step = self.steps[step](self.content_frame)
        self.current_step.pack(fill="both", expand=True)
        
        if step == 0:
            # first step
            self.back_button["state"] = DISABLED
            self.next_button["state"] = NORMAL
            self.finish_button["state"] = DISABLED

        elif step == len(self.steps)-1:
            # last step
            self.back_button["state"] = NORMAL
            self.next_button["state"] = DISABLED
            self.finish_button["state"] = NORMAL

        else:
            # all other steps
            self.back_button["state"] = NORMAL
            self.next_button["state"] = NORMAL
            self.finish_button["state"] = DISABLED

    def next(self):
        self.current_step.perform_action()
        self.show_step(self.step_no + 1)

    def back(self):
        self.show_step(self.step_no - 1)

    def finish(self):
        print("Closing Installer")
        self.root.quit()
        self.root.destroy()


if __name__ == '__main__':
    glob.set_application_folder(os.path.dirname(os.path.realpath(__file__)))
    wiz = Wizard()
    print("Installer finished")
    