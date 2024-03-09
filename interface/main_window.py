# Import libraries
import customtkinter as ctk
# Import title_frame
from .title_field import TitleField
# Import data_load_field
from .data_load_field import DataLoadField
# Import drawing_type_field
from. drawing_type_field import DrawingTypeField
# Import ls_setting_field
from .ls_setting_field import LSSettingField
# Import lss_setting_field
from .css_setting_field import CSSSettingField
# Import drawing btn field
from .draw_btn_field import DrawingButtonField

# Main window class -> Class
class MainWindow(ctk.CTk):
    # Class constructor -> Method
    def __init__(self):

        self.__data_load_field = None
        self.__drawing_type_field = None
        self.__ls_setting_field = None
        self.__css_setting_field = None
        self.__drawing_btn_field = None

        # Super
        super().__init__()

        # Set title
        self.title('Auto Drawer')

        # Set grid layout
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)

        self.grid_rowconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=2)
        self.grid_rowconfigure(index=2, weight=2)
        self.grid_rowconfigure(index=3, weight=2)
        self.grid_rowconfigure(index=4, weight=1)

        # Set window size
        self.geometry('800x500')
        
        # Add title field
        self.title_field = TitleField(master=self)
        # Add data load field
        self.__data_load_field = DataLoadField(master=self)
        # Add drawing type selector field
        self.__drawing_type_field = DrawingTypeField(master=self)
        # Add ls setting field
        self.__ls_setting_field = LSSettingField(master=self)
        # Add css setting field
        self.__css_setting_field = CSSSettingField(master=self)
        # Add drawing button
        self.__drawing_btn_field = DrawingButtonField(master=self)

        # Run loop
        self.mainloop()
    
    @property
    def get_data_load_field(self):
        return self.__data_load_field
    
    @property
    def get_drawing_type_field(self):
        return self.__drawing_type_field
    
    @property
    def get_ls_setting_field(self):
        return self.__ls_setting_field
    
    @property
    def get_css_setting_field(self):
        return self.__css_setting_field

    @property
    def get_drawing_btn_field(self):
        return self.__drawing_btn_field