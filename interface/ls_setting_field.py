# Import libraries
# Import customtkinter
import customtkinter as ctk
# Import setting
from .settings import Settings as set

# LS Setting class -> Class
class LSSettingField(ctk.CTkFrame):
    # Class constructor -> Method
    def __init__(self, master):

        self.__master = master

        # Supper
        super().__init__(master=self.__master)
        
        # Setup grid layout
        self.grid_columnconfigure(index=0, weight=2)
        self.grid_columnconfigure(index=1, weight=5)
        self.grid_columnconfigure(index=2, weight=1)

        self.grid_rowconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)
        self.grid_rowconfigure(index=2, weight=1)
        self.grid_rowconfigure(index=3, weight=1)

        # Set title
        self.__title_lbl = ctk.CTkLabel(master=self, text='Section 03 - Setting LS Values', font=set.H2_FONT, height=set.HEIGHT, anchor='w')
        self.__title_lbl.grid(column=0, row=0, columnspan=3, padx=(10, 10), pady=(5, 5), sticky='ew')

        # Set vertiacal scale label
        self.__vertical_scale_lbl = ctk.CTkLabel(master=self, text='Vertical Scale:', height=set.HEIGHT, anchor='e')
        self.__vertical_scale_lbl.grid(column=0, row=1, padx=(10, 5), pady=(5, 5), sticky='ew')

        # Set Vertical Scale
        self.__vertical_scale = ctk.IntVar(value=100)
        self.__vertical_scale_entry = ctk.CTkEntry(master=self, textvariable=self.__vertical_scale,  height=set.HEIGHT)
        self.__vertical_scale_entry.grid(column=1, row=1, padx=(5, 5), pady=(5, 5), sticky='ew')

        # Set horizontal scale label
        self.__horizontal_scale_lbl = ctk.CTkLabel(master=self, text='Horizontal Scale:', height=set.HEIGHT, anchor='e')
        self.__horizontal_scale_lbl.grid(column=0, row=2, padx=(10, 5), pady=(5, 5), sticky='ew')

        # Sethorizontal Scale
        self.__horizontal_scale = ctk.IntVar(value=1000)
        self.__horizontal_scale_entry = ctk.CTkEntry(master=self, textvariable=self.__horizontal_scale, height=set.HEIGHT)
        self.__horizontal_scale_entry.grid(column=1, row=2, padx=(5, 5), pady=(5, 5), sticky='ew')

        # Set tbm label
        self.__tbm_lbl = ctk.CTkLabel(master=self, text='TBM Value:', height=set.HEIGHT, anchor='e', state=ctk.DISABLED)
        self.__tbm_lbl.grid(column=0, row=3, padx=(10, 5), pady=(5, 5), sticky='ew')

        # Set tbm value
        self.__tbm = ctk.IntVar(value=0)
        self.__tbm_entry = ctk.CTkEntry(master=self, textvariable=self.__tbm, height=set.HEIGHT, state=ctk.DISABLED)
        self.__tbm_entry.grid(column=1, row=3, padx=(5, 5), pady=(5, 5), sticky='ew')

        # Set tbm auto
        self.__tbm_check_val = ctk.StringVar(value='on')
        self.__tbm_auto_ckeckb = ctk.CTkCheckBox(master=self, text='Auto', height=set.HEIGHT, variable=self.__tbm_check_val, onvalue='on', offvalue='off', command=self.__checkbox_check)
        self.__tbm_auto_ckeckb.grid(column=2, row=3, padx=(5, 10), pady=(5, 5), sticky='ew')

        # Set to grid
        self.grid(column=0, row=3, padx=(10, 5), pady=(5, 5), sticky='wne')
    

    # Checkbox command
    def __checkbox_check(self):
        # If cheked
        if (self.__tbm_check_val.get() == 'on'):
            self.__tbm_entry.configure(state=ctk.NORMAL)

        # If not cheked
        elif (self.__tbm_check_val.get() == 'off'):
            self.__tbm_entry.configure(state=ctk.DISABLED)

    # Get vertical scale
    @property
    def get_v_scale(self) -> int:
        return self.__vertical_scale.get()
    
    # Get horizontal scale
    @property
    def get_h_scale(self):
        return self.__horizontal_scale.get()

    # Get tbm value
    @property
    def get_tbm(self):
        # If tbm is auto
        if (self.__tbm_check_val.get() == 'on'):
            return None
        # If tbm value available
        elif (self.__tbm_check_val.get() == 'off'):
            return self.__tbm