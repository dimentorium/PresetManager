from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog, filedialog

import textwrap

import pickle

import reaper.preset as rp
import reapy
import core.ui as ui

import copy

class main_view():
    def __init__(self):
        self.preset_list = {}
        self._search_filter = ""
        self.root = Tk()
        self.root.title("Reaper Preset Manager")
        
        current_row = 0

        #Buttons for handling database
        self.btn_new_database = Button(self.root,text="New Database", command=self.new_database)
        self.btn_new_database.grid(row=current_row,column=0, padx=5, pady=5, sticky='ew')

        self.btn_load_database = Button(self.root,text="Load Database", command=self.load_database)
        self.btn_load_database.grid(row=current_row,column=1, padx=5, pady=5, sticky='ew')

        self.btn_save_database = Button(self.root,text="Save Database", command=self.save_database)
        self.btn_save_database.grid(row=current_row,column=2, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Separator
        Separator(self.root,orient="horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Buttons for handling presets
        self.btn_load_preset = Button(self.root,text="Load Preset", command=self.load_preset)
        self.btn_load_preset.grid(row=current_row,column=0, padx=5, pady=5, sticky='ew')
        
        self.btn_save_preset = Button(self.root,text="Save Preset", command=self.save_preset)
        self.btn_save_preset.grid(row=current_row,column=1, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Separator
        Separator(self.root,orient="horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Search Field
        Label(self.root,text="Search").grid(row=current_row, padx=5, column=0, sticky='w')
        
        self._entry_text = StringVar()
        self._entry_text.trace("w", self.search)
        self.search_box = Entry(self.root, textvariable=self._entry_text)
        self.search_box.grid(row=current_row, column=1,columnspan=3, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Separator
        Separator(self.root,orient="horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')
        current_row +=1

        #Treeview for presets
        self.presettree = Treeview(self.root)
        self.presettree.grid(row=current_row, rowspan=8, columnspan=3, padx=5, pady=5, sticky='ew')
        self.presettree.bind("<ButtonRelease-1>", self.select_item)
        self.presettree["columns"] = ("Plugin")
        self.presettree.heading("#0", text="Preset")
        self.presettree.heading("Plugin", text="Plugin")
        vsb = Scrollbar(self.root, orient="vertical", command=self.presettree.yview)
        vsb.grid(row=current_row, rowspan=8, column=3, pady=5,sticky='nsw')
        self.presettree.configure(yscrollcommand=vsb.set)
        current_row +=8

        #Separator
        Separator(self.root,orient="horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')

        self.update_ui()      

        #self.simulate_db()  

    def search(self, *args):
        self._search_filter = self._entry_text.get()
        self.update_list()
        self.update_ui()
    
    def show(self):
        #keep window on top of all others
        self.root.wm_attributes("-topmost", 1)
        self.root.mainloop()
    
    def save_preset(self):
        #test = ui.SavePreset(self.root).selection
        project = reapy.Project()
        if project.n_selected_tracks > 0:
            preset_name = simpledialog.askstring("Input", "Please enter preset Name", parent=self.root)
            if preset_name != None and preset_name != "":
                newpreset = rp.save(preset_name)
                self.preset_list[preset_name] = newpreset
                self.update_list()
            else:
                simpledialog.messagebox.showinfo("Warning", "Please enter Name")
        else:
            simpledialog.messagebox.showinfo("Warning", "Please select Track")

        self.update_ui()
            


    def load_preset(self):
        item = self.presettree.item(self.presettree.focus())
        index = item["text"]
        rp.load(self.preset_list[index])
        self.update_ui()

    def save_database(self):
        filename = filedialog.asksaveasfilename(title = "Select file",filetypes = (("database","*.bin"),("all files","*.*")))
        pickle.dump(self.preset_list, open(filename,"wb"))
        self.update_ui()

    def load_database(self):
        filename = filedialog.askopenfilename(title = "Select file",filetypes = (("database","*.bin"),("all files","*.*")))
        self.preset_list = pickle.load( open( filename, "rb" ) )
        self.update_list()
        self.update_ui()

    def new_database(self):
        self.preset_list = {}
        self.update_list()
        self.update_ui()

    def select_item(self, evt):
        self.update_ui()


    def update_list(self):
        self.presettree.delete(*self.presettree.get_children())
        for preset in self.preset_list:
            show = True
            if self._search_filter != "":
                show = self._search_filter in self.preset_list[preset].preset_name

            if show:
                self.presettree.insert("", END, 
                                        text=self.preset_list[preset].preset_name, 
                                        values=(self.preset_list[preset].plugin_name,))

    def update_ui(self):
        #======================== Update Save Database Button ====================
        if len(self.preset_list) == 0:
            self.btn_save_database['state'] = DISABLED
        else:
            self.btn_save_database['state'] = NORMAL

        #======================== Update Load Preset Button ====================
        if len(self.presettree.selection()) == 0:
            self.btn_load_preset['state'] = DISABLED
        else:
            self.btn_load_preset['state'] = NORMAL

    def simulate_db(self):
        newpreset = rp.save("test_db_")
        for i in range(10000):
            copy_preset = copy.copy(newpreset)
            copy_preset.preset_name = "test_db_" + str(i)
            self.preset_list[copy_preset.preset_name] = copy_preset
        self.update_list()

        
mv = main_view()
mv.show()




