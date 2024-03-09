# Import libraires
import customtkinter as ctk
from tkinter import messagebox
# Import Setting
from .settings import Settings as set
# Import data manager
from backend.data_manager import DataManager
from backend.drawing_manager import DrawingManager

# Drawing button class -> Class
class DrawingButtonField(ctk.CTkFrame):
    # Class constructor -> Method
    def __init__(self, master):

        # Master 
        self.__master = master

        # Supper
        super().__init__(master=self.__master)

        # Set grid
        self.grid_columnconfigure(index=0, weight=5)
        self.grid_columnconfigure(index=1, weight=1)

        self.grid_rowconfigure(index=0, weight=1)

        # Add drawing button
        self.__drawing_btn = ctk.CTkButton(master=self, text='Draw', height=set.HEIGHT, command=self.__draw)
        self.__drawing_btn.grid(column=1, row=0, padx=(5, 10), pady=(10, 10), sticky='we')

        # Add to the grid
        self.grid(column=0, row=4, columnspan=2, padx=(10, 10), pady=(5, 10), sticky='wne')
    
    # Draw button command
    def __draw(self):
        # Initilize data manager
        try:
            dm = DataManager(data_file=self.__master.get_data_load_field.get_file)
        except:
            messagebox.showerror(title='Data File Error', message='Somthing is wrong in data file. Data file not loaded. Try again')
        
        # Inizialize drawing manager
        drawing = DrawingManager()

        # Get drawing type
        drawing_type: str = self.__master.get_drawing_type_field.get_drawing_type
        # Get drawing ls vertical scale
        ls_v_scale: int = self.__master.get_ls_setting_field.get_v_scale
        # Get drawing ls horizontal scale
        ls_h_scale: int = self.__master.get_ls_setting_field.get_h_scale
        # Get ls tbm
        ls_tbm: float = self.__master.get_ls_setting_field.get_tbm
        # Get drawing css vertical scale
        css_v_scale: int = self.__master.get_css_setting_field.get_v_scale
        # Get drawing css horizontal scale
        css_h_scale: int = self.__master.get_css_setting_field.get_h_scale
        # Get css tbm
        css_tbm: float = self.__master.get_css_setting_field.get_tbm

        # Draw
        try:
            drawing.draw(
                drawing_type=drawing_type,
                ls_data=dm.get_ls_data,
                cs_data=dm.get_css_data,
                ls_base=(0.0, 0.0),
                css_base=(0.0, 0.0),
                ls_tbm=ls_tbm,
                css_tbm=css_tbm,
                ls_v_scale=ls_v_scale,
                ls_h_scale=ls_h_scale,
                css_h_scale=css_h_scale,
                css_v_scale=css_v_scale,
                ls_title=''
                )
        except Exception as ex:
            messagebox.showerror(title='Drawing Error', message='Somthing is wrong in drawing file. Drawing file not created')
            print(ex)