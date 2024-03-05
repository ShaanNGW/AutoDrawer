# Import DataManager
from backend import DataManager
from backend import DrawingManager
import pandas as pd

if (__name__ == '__main__'):

    # File Location Here
    file_location: str = 'data_template.ods'

    dm = DataManager(data_file=file_location)
    drawing = DrawingManager()
    drawing.draw(drawing_type=DrawingManager.LS_AND_CSS, ls_data=dm.get_ls_data, cs_data=dm.get_css_data)