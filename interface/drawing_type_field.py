# Import Libraries
# Import customtkinter
import customtkinter as ctk
# Import setting
from .settings import Settings as set

# Drawing type selection field -> Class
class DrawingTypeField(ctk.CTkFrame):
    # Class constructor -> Method
    def __init__(self, master):

        self.__master = master
        # Drawing type
        self.__type = 'ls_and_css'

        # Super
        super().__init__(master=self.__master)

        # Set grid layout
        self.grid_columnconfigure(index=0, weight=1)

        self.grid_rowconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)

        # Set title
        self.__title_lbl = ctk.CTkLabel(master=self, text='Section 02 - Drawing Type Selector', font=set.H2_FONT, height=set.HEIGHT, anchor='w')
        self.__title_lbl.grid(column=0, row=0, padx=(10, 10), pady=(5, 5), sticky='ew')

        # Set Drop box
        self.__drawing_type_val: list[str] = ['LS and CSS', 'LS Only', 'CSS Only']
        self.__drawing_type_cb = ctk.CTkComboBox(master=self, values=self.__drawing_type_val, height=set.HEIGHT, command=self.__type_select)
        self.__drawing_type_cb.grid(column=0, row=1, padx=(10, 10), pady=(5, 5), sticky='ew')

        # Add to gird
        self.grid(column=0, row=2, columnspan=2, padx=(10, 10), pady=(5, 5), sticky='enw')
    
    # Drawing type selector trigger -> Method
    def __type_select(self, choise):

        # If drawing type ls and css
        if (choise == 'LS and CSS'):
            self.__type = 'ls_and_css'

        # If choise is ls only
        elif (choise == 'LS Only'):
            self.__type = 'ls_only'

        # If choise is css only
        elif (choise == 'CSS Only'):
            self.__type = 'css_only'
    
    # Get drawing type
    @property
    def get_drawing_type(self):
        return self.__type