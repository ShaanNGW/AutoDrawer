# Import libraries
from typing import Any, Tuple
import customtkinter as ctk
# Import file dialog
from customtkinter import filedialog

# Import setting
from .settings import Settings as set

# DataLoadField class -> Class
class DataLoadField(ctk.CTkFrame):
    # Class constructor -> Method
    def __init__(self, master):

        self.__master = master
        self.__file = ''

        # File location
        self.__file_location: str = None

        # Super
        super().__init__(master=self.__master)

        # Set grid
        self.grid_columnconfigure(index=0, weight=5)
        self.grid_columnconfigure(index=1, weight=1)

        self.grid_rowconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=2)

        # Add field title
        self.__section_title_lbl = ctk.CTkLabel(master=self, text='Section 01 - Data Select', font=set.H2_FONT, height=set.HEIGHT, anchor='w')
        self.__section_title_lbl.grid(column=0, row=0, columnspan=2, padx=(10, 10), pady=(5, 5), sticky='enw')

        # Add data load field
        self.__file_location: str = ctk.StringVar(value='')
        self.__data_load = ctk.CTkEntry(master=self, textvariable=self.__file_location,  height=set.HEIGHT)
        self.__data_load.grid(column=0, row=1, padx=(10, 5), pady=(10, 10), sticky='ew')

        # Add button for file dialog
        self.__open_btn = ctk.CTkButton(master=self, text='Select', font=set.NORMAL_FONT,  height=set.HEIGHT, command=self.__select_file)
        self.__open_btn.grid(column=1, row=1, padx=(5, 10), pady=(10, 10), sticky='ew')

        # Add to grid
        self.grid(column=0, row=1, columnspan=2, padx=(10, 10), pady=(5, 5), sticky='enw')
    
    # File Select command
    def __select_file(self):
        # Get file name
        file_location = filedialog.askopenfilename(title='Select Data File', filetypes=(('Excel', '*.xlsx'), ('Libra Cal', '*.ods'), ('All Files', '*.*')))
        # Set file name in entry
        self.__file_location.set(value=file_location)
        # Set value to file
        self.__file = file_location
    
    # File location
    @property
    def get_file(self):
        return self.__file