from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog, filedialog

import textwrap

import pickle

import reaper.preset as rp
import reapy
import core.ui as ui
import core.items as items

import copy

class main_view():
    def __init__(self):
        self.preset_list = {}
        self._search_filter = ""
        self._selected_item = None
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
        self.presettree.bind("<<TreeviewSelect>>", self.select_item)
        self.presettree["columns"] = ("Plugin")
        self.presettree.heading("#0", text="Preset")
        self.presettree.heading("Plugin", text="Plugin")
        vsb = Scrollbar(self.root, orient="vertical", command=self.presettree.yview)
        vsb.grid(row=current_row, rowspan=8, column=3, pady=5,sticky='nsw')
        self.presettree.configure(yscrollcommand=vsb.set)
        current_row +=8

        #Treeview for presets
        self.presetinfo = Treeview(self.root)
        self.presetinfo.grid(row=current_row, rowspan=2, columnspan=3, padx=5, pady=5, sticky='ew')
        self.presetinfo["columns"] = ("Value")
        self.presetinfo.heading("#0", text="Property")
        self.presetinfo.heading("Value", text="Value")
        current_row +=4

        #Separator
        Separator(self.root,orient="horizontal").grid(row=current_row, columnspan=4, padx=5, pady=5, sticky='ew')

        self.update_ui()      

        #keep window on top of all others
        self.root.wm_attributes("-topmost", 1)
        self.root.mainloop()

    def search(self, *args):
        self._search_filter = self._entry_text.get()
        self.update_list()
        self.update_ui()        
    
    def save_preset(self):
        project = reapy.Project()
        if project.n_selected_tracks > 0:
            cancelled, result = ui.save_preset_dialog(self.root)
            if not cancelled:
                newpreset = rp.save(result[0])
                vsti_item = items.vstipreset(result[0], newpreset, result[1])
                self.preset_list[result[0]] = vsti_item
                self.update_list()
            else:
                simpledialog.messagebox.showinfo("Warning", "Please enter Name")
        else:
            simpledialog.messagebox.showinfo("Warning", "Please select Track")

        self.update_ui()
            


    def load_preset(self):
        self._selected_item.load()
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
        selected_item = self.presettree.item(self.presettree.focus())
        index = selected_item["text"]
        self._selected_item = self.preset_list[index]

        self.update_info()
        self.update_ui()

    def update_info(self):
        self.presetinfo.delete(*self.presetinfo.get_children())
        if self._selected_item != None:
            for key, value in self._selected_item.properties.items():
                self.presetinfo.insert("", END, text=key, values=(value,))

    def update_list(self):
        self.presettree.delete(*self.presettree.get_children())
        for preset in self.preset_list:
            show = True
            if self._search_filter != "":
                show = self.preset_list[preset].check_filter(self._search_filter)

            if show:
                self.presettree.insert("", END, 
                                        text=self.preset_list[preset].preset_name, 
                                        values=(self.preset_list[preset].chunk.plugin_name,))

    def update_ui(self):
        if len(self.presettree.selection()) == 0:
            self._selected_item = None
        #======================== Update Save Database Button ====================
        if len(self.preset_list) == 0:
            self.btn_save_database['state'] = DISABLED
        else:
            self.btn_save_database['state'] = NORMAL

        #======================== Update Load Preset Button ====================
        if self._selected_item == None:
            self.btn_load_preset['state'] = DISABLED
        else:
            self.btn_load_preset['state'] = NORMAL


#===========================Start Main Function================================#       
mv = main_view()




