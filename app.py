# Import DataManager
from backend import DataManager
from backend import DrawingManager
import pandas as pd

if (__name__ == '__main__'):
    dm = DataManager('data_template.ods')
    drawing = DrawingManager()
    point = drawing.draw_ls(ls_data=dm.get_ls_data, title='sdadasd asdasdasd asdasdas')
    drawing.draw_css(css_data=dm.get_css_data, base_point=point)
