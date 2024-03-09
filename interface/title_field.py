# Import libraries
import customtkinter as ctk

# Import setting
from .settings import Settings as set

# TitleField class -> Class
class TitleField(ctk.CTkFrame):
    # Class constructor -> Method
    def __init__(self, master) -> None:

        self.__master = master

        # Super
        super().__init__(master=self.__master)

        # Add Title -> Label
        self.__title_label = ctk.CTkLabel(master=self, text='Auto Drawer', font=set.H1_FONT)
        self.__title_label.pack(pady=(5, 5))

        # Set to main window
        self.grid(column=0, row=0, columnspan=2, padx=(10, 10), pady=(10, 5), sticky='enw')