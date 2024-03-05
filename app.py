# Import DataManager
from backend import DataManager
from backend import DrawingManager
import pandas as pd

if (__name__ == '__main__'):

    # File Location Here
    file_location: str = ''

    dm = DataManager(file_location)
    drawing = DrawingManager()
    point = drawing.draw_ls(ls_data=dm.get_ls_data, title='')
    drawing.draw_css(css_data=dm.get_css_data, base_point=point)
