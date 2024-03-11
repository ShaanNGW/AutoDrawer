# Import libraries
# Import ezdxf
import ezdxf
# Import units and colors
from ezdxf import units, colors
from ezdxf.enums import TextEntityAlignment
# Import point
from .point import Point as pt
from .ls import LS
from .cs import CSS

# DrawingManager class -> Class
class DrawingManager:

    # Litarals
    # Colors
    BLACK = 7  # colors.rgb2int(rgb=(0, 0, 0))
    WHITE = 7  # colors.rgb2int(rgb=(225, 225, 225))
    RED = 1  # colors.rgb2int(rgb=(225, 0, 0))
    YELLOW = 2  # colors.rgb2int(rgb=(255, 255, 0))
    BLUE = 5  # colors.rgb2int(rgb=(0, 0, 255))
    GREEN = 3  # colors.rgb2int(rgb=(0, 255, 0))
    CYEN = 4  # colors.rgb2int(rgb=(0, 255, 255))
    PINK = 6  # colors.rgb2int(rgb=(255, 105, 180))

    # CDrawing types
    LS_AND_CSS: str = 'ls_and_css'
    LS: str = 'ls_only'
    CSS: str = 'css_only'

    # Class constructor -> Method
    def __init__(self) -> None:
        
        # Set value
        self.__drawing_text_height: float = pt.to_meter(value=3.0, unit=pt.MM)
        self.__text_title_height: float = pt.to_meter(value=5.0, unit=pt.MM)
        self.__text_gap: float = pt.point(0.0, pt.to_meter(value=1.0, unit=pt.MM))
        self.__drawing_gap = pt.point(pt.to_meter(value=50.0, unit=pt.MM), 0.0)
        
        self.__detail_line_gap: float = pt.point(0.0, pt.to_meter(value=20.0, unit=pt.MM))
        self.__detail_line_width: float = pt.point(pt.to_meter(value=50, unit=pt.MM), 0.0)
        self.__extra_line_width: float = pt.point(pt.to_meter(value=10, unit=pt.MM), 0.0)

        # Make ezdxf object
        self.__doc = ezdxf.new('R12')
        # Set drawing unit
        self.__doc.header['$INSUNITS'] = units.M

        # Set drawing layers
        self.__layer_normal_text = self.__doc.layers.add(name='NORMAL_TEXT', color=self.WHITE)
        self.__layer_title_text = self.__doc.layers.add(name='TITLE_TEXT', color=self.WHITE)
        self.__layer_detail_line = self.__doc.layers.add(name='DETAIL_LINES', color=self.WHITE)
        self.__layer_height_line = self.__doc.layers.add(name='HIGHT_LINE', color=self.WHITE)
        self.__layer_description_line = self.__doc.layers.add(name='DESCRIPTION_LINE', color=self.BLUE)
        self.__layer_description_text = self.__doc.layers.add(name='DESCRIPTION_TEXT', color=self.RED)
        self.__layer_ground_line = self.__doc.layers.add(name='GROUND_LINE', color=self.CYEN)

        # Set work space
        self.__msp = self.__doc.modelspace()
    
    # Draw ls -> Method
    def __draw_ls(self, ls_data: list, base_point: tuple, v_scale: int, h_scale: int, tbm: float, title: str) -> tuple:

        # If tbm is None
        if (tbm == None):
            ls_tbm: float = LS.get_tbm(ls_list=ls_data)
        # If not
        else:
            ls_tbm: float = tbm
        
        # Line 01
        line_01_start: pt.point = base_point
        line_01_end: pt.point = pt.add_point(line_01_start, self.__detail_line_width, pt.point(pt.scale(value=LS.get_max_chainage(ls_list=ls_data), scale=h_scale), 0.0), self.__extra_line_width)
        line_01 = self.__msp.add_line(start=line_01_start, end=line_01_end, dxfattribs={'layer': self.__layer_detail_line, 'color': 256})

        # Line 01 Text
        line_01_txt_str: str = 'Chainage (m)'
        line_01_txt_point = pt.add_point(line_01_start, self.__text_gap)
        line_01_txt = self.__msp.add_text(text=line_01_txt_str, height=self.__drawing_text_height, dxfattribs={'layer': self.__layer_normal_text, 'color': 256}).set_placement(line_01_txt_point)

        # Line 02
        line_02_start = pt.add_point(line_01_start, self.__detail_line_gap)
        line_02_end = pt.add_point(line_01_end, self.__detail_line_gap)
        line_02 = self.__msp.add_line(start=line_02_start, end=line_02_end, dxfattribs={'layer': self.__layer_detail_line, 'color': 256})

        # Line 02 Text
        line_02_txt_str: str = 'Redused Level (m)'
        line_02_txt_point = pt.add_point(line_02_start, self.__text_gap)
        line_02_txt = self.__msp.add_text(text=line_02_txt_str, height=self.__drawing_text_height, dxfattribs={'layer': self.__layer_normal_text, 'color': 256}).set_placement(line_02_txt_point)

        # Line 03
        line_03_start = pt.add_point(line_02_start, self.__detail_line_gap)
        line_03_end = pt.add_point(line_02_end, self.__detail_line_gap)
        line_03 = self.__msp.add_line(start=line_03_start, end=line_03_end, dxfattribs={'layer': self.__layer_detail_line, 'color': 256})
        
        # Line 03 Text
        line_03_txt_str: str = f'TBM: {ls_tbm:.2f}m'
        line_03_txt_point = pt.add_point(line_03_start, self.__text_gap)
        line_03_txt = self.__msp.add_text(text=line_03_txt_str, height=self.__drawing_text_height, dxfattribs={'layer': self.__layer_normal_text, 'color': 256}).set_placement(line_03_txt_point)

        # Temparary base
        temp_base = pt.add_point(line_01_start, self.__detail_line_width)
        # Temparary drawing base
        temp_drawing_base = pt.add_point(temp_base, self.__detail_line_gap, self.__detail_line_gap)
        # Ground level points
        temp_ground: list = []

        # Draw values
        for ls in ls_data:

            # Max redused
            max_redused: float = pt.scale(value=(LS.get_max_redused(ls_list=ls_data) - ls_tbm), scale=v_scale)

            # Set Chainage
            chainage_text: str = f'{ls.get_chainage:.3f}'
            chainage_point = pt.add_point(temp_base, pt.point(pt.scale(value=ls.get_chainage, scale=h_scale), 0.0), pt.point((self.__drawing_text_height/2), 0.0), self.__text_gap)
            chainage = self.__msp.add_text(text=chainage_text, height=self.__drawing_text_height, rotation=90.0, dxfattribs={'layer': self.__layer_normal_text, 'color': 256}).set_placement(chainage_point)

            # Set Redused
            redused_text: str = f'{ls.get_reduced:.3f}'
            redused_point = pt.add_point(temp_base, pt.point(pt.scale(value=ls.get_chainage, scale=h_scale), 0.0), pt.point((self.__drawing_text_height/2), 0.0), self.__text_gap, self.__detail_line_gap)
            redused = self.__msp.add_text(text=redused_text, height=self.__drawing_text_height, rotation=90.0, dxfattribs={'layer': self.__layer_normal_text, 'color': 256}).set_placement(redused_point)

            # Diduct redused
            diduct_redused = pt.scale(value=ls.get_reduced, scale=v_scale) - pt.scale(value=ls_tbm, scale=v_scale)

            # Set lines
            line_start = pt.add_point(temp_drawing_base, pt.point(pt.scale(value=ls.get_chainage, scale=h_scale), 0.0))
            line_end = pt.add_point(line_start, pt.point(0.0, diduct_redused))
            line = self.__msp.add_line(start=line_start, end=line_end, dxfattribs={'layer': self.__layer_height_line, 'color': 256})

            # Description Line
            des_line_start = line_end
            des_line_end = pt.add_point(line_start, pt.point(0.0, (max_redused + pt.to_meter(value=50.0, unit=pt.MM))))
            des_line = self.__msp.add_line(start=des_line_start, end=des_line_end, dxfattribs={'layer': self.__layer_description_line, 'color': 256})

            # Set description
            des_txt_str: str = ls.get_description
            des_txt_point = pt.add_point(des_line_end, self.__text_gap)
            des_txt = self.__msp.add_text(text=des_txt_str, height=self.__drawing_text_height, rotation=45.0, dxfattribs={'layer': self.__layer_description_text, 'color': 256}).set_placement(des_txt_point)
            
            # Add end point to list
            temp_ground.append(line_end)
        
        # Draw ground
        ground = self.__msp.add_polyline2d(points=temp_ground, dxfattribs={'layer': self.__layer_ground_line, 'color': 256})

        # Set title
        title_text_str: str = f'LS of {title}'
        title_text_point = pt.add_point(pt.center(start=line_01_start, end=line_01_end), pt.point(0.0, -pt.to_meter(value=20.0, unit=pt.MM)))
        title_text = self.__msp.add_text(text=title_text_str, height=self.__text_title_height, dxfattribs={'layer': self.__layer_title_text, 'color': 256}).set_placement(title_text_point, align=TextEntityAlignment.MIDDLE)

        # Set Scale Horizontal
        h_scale_text_str: str = f'Horizontal Scale 1:{h_scale}'
        h_scale_text_point = pt.add_point(line_01_end, pt.point(0.0, -pt.to_meter(value=10.0, unit=pt.MM)), pt.point(0.0, -pt.to_meter(value=20.0, unit=pt.MM)))
        h_scale_text = self.__msp.add_text(text=h_scale_text_str, height=self.__drawing_text_height, dxfattribs={'layer': self.__layer_normal_text, 'color': 256}).set_placement(h_scale_text_point, align=TextEntityAlignment.RIGHT)
        
        # Set Scale Horizontal
        v_scale_text_str: str = f'Vertical Scale 1:{v_scale}'
        v_scale_text_point = pt.add_point(h_scale_text_point, pt.point(0.0, -pt.to_meter(value=5.0, unit=pt.MM)))
        v_scale_text = self.__msp.add_text(text=v_scale_text_str, height=self.__drawing_text_height, dxfattribs={'layer': self.__layer_normal_text, 'color': 256}).set_placement(v_scale_text_point, align=TextEntityAlignment.RIGHT)

        return line_01_end
    
    # Draw ls -> Method
    def __draw_css(self, css_data: list, base_point=pt.point(0.0, 0.0), v_scale: int=100, h_scale: int=100, tbm: float=None) -> tuple:
        
        # If tbm is None
        if (tbm == None):
            cs_tbm: float = CSS.get_tbm(css_data=css_data)
        # If not
        else:
            cs_tbm: float = tbm
        
        # If base point is (0.0, 0.0)
        if (base_point == pt.point(0.0, 0.0)):
            new_base = pt.point(0.0, 0.0)
        else:
            new_base = pt.add_point(base_point, self.__drawing_gap)

        # Draw css
        for cs in css_data:

            # Max offset width
            offset_width = pt.scale(value=cs.get_offset_width(), scale=h_scale)

            # Line 01
            line_01_start = new_base
            line_01_end = pt.add_point(line_01_start, self.__detail_line_width, pt.point(offset_width, 0.0), self.__extra_line_width)
            line_01 = self.__msp.add_line(start=line_01_start, end=line_01_end, dxfattribs={'layer': self.__layer_detail_line})

            # Line 01 Text
            line_01_txt_str: str = 'Chainage (m)'
            line_01_txt_point = pt.add_point(line_01_start, self.__text_gap)
            line_01_txt = self.__msp.add_text(text=line_01_txt_str, height=self.__drawing_text_height, dxfattribs={'layer': self.__layer_normal_text}).set_placement(line_01_txt_point)

            # Line 02
            line_02_start = pt.add_point(line_01_start, self.__detail_line_gap)
            line_02_end = pt.add_point(line_01_end, self.__detail_line_gap)
            line_02 = self.__msp.add_line(start=line_02_start, end=line_02_end, dxfattribs={'layer': self.__layer_detail_line})

            # Line 02 Text
            line_02_txt_str: str = 'Redused Level (m)'
            line_02_txt_point = pt.add_point(line_02_start, self.__text_gap)
            line_02_txt = self.__msp.add_text(text=line_02_txt_str, height=self.__drawing_text_height, dxfattribs={'layer': self.__layer_normal_text}).set_placement(line_02_txt_point)

            # Line 03
            line_03_start = pt.add_point(line_02_start, self.__detail_line_gap)
            line_03_end = pt.add_point(line_02_end, self.__detail_line_gap)
            line_03 = self.__msp.add_line(start=line_03_start, end=line_03_end, dxfattribs={'layer': self.__layer_detail_line})
            
            # Line 03 Text
            line_03_txt_str: str = f'TBM: {cs_tbm:.2f}m'
            line_03_txt_point = pt.add_point(line_03_start, self.__text_gap)
            line_03_txt = self.__msp.add_text(text=line_03_txt_str, height=self.__drawing_text_height, dxfattribs={'layer': self.__layer_normal_text}).set_placement(line_03_txt_point)

            # Set title
            cs_title_text_str: str = f'{cs.get_chainage:.3f}m'
            cs_title_text_point = pt.add_point(new_base, pt.center(start=line_01_start, end=line_01_end), pt.point(0.0, -pt.to_meter(value=20.0, unit=pt.MM)))
            cs_title_text = self.__msp.add_text(text=cs_title_text_str, height=self.__text_title_height, dxfattribs={'layer': self.__layer_title_text}).set_placement(cs_title_text_point, align=TextEntityAlignment.MIDDLE)

            # Set Scale Horizontal
            h_scale_text_str: str = f'Horizontal Scale 1:{h_scale}'
            h_scale_text_point = pt.add_point(line_01_end, pt.point(0.0, -pt.to_meter(value=10.0, unit=pt.MM)), pt.point(0.0, -pt.to_meter(value=20.0, unit=pt.MM)))
            h_scale_text = self.__msp.add_text(text=h_scale_text_str, height=self.__drawing_text_height, dxfattribs={'layer': self.__layer_normal_text}).set_placement(h_scale_text_point, align=TextEntityAlignment.RIGHT)
            
            # Set Scale Horizontal
            v_scale_text_str: str = f'Vertical Scale 1:{v_scale}'
            v_scale_text_point = pt.add_point(h_scale_text_point, pt.point(0.0, -pt.to_meter(value=5.0, unit=pt.MM)))
            v_scale_text = self.__msp.add_text(text=v_scale_text_str, height=self.__drawing_text_height, dxfattribs={'layer': self.__layer_normal_text}).set_placement(v_scale_text_point, align=TextEntityAlignment.RIGHT)

            # Set css ground points
            cs_grounds: list = []

            # Draw height lines
            for data in range(len(cs.get_offsets)):

                # Set drawing base
                drawing_base = pt.add_point(new_base, self.__detail_line_width, self.__detail_line_gap, self.__detail_line_gap, pt.point(pt.scale(value=abs(min(cs.get_offsets)), scale=h_scale), 0.0))
                # Set text base
                text_base = pt.add_point(new_base, self.__detail_line_width, pt.point(pt.scale(value=abs(min(cs.get_offsets)), scale=h_scale), 0.0))

                # Set chainage label
                cs_chainage_text: str = f'{cs.get_offsets[data]:.3f}'
                cs_chainage_point = pt.add_point(text_base, pt.point(pt.scale(value=cs.get_offsets[data], scale=h_scale), 0.0), self.__text_gap)
                cs_chainage = self.__msp.add_text(text=cs_chainage_text, height=self.__drawing_text_height, rotation=90.0, dxfattribs={'layer': self.__layer_normal_text}).set_placement(cs_chainage_point)

                # Set Redused
                cs_redused_text: str = f'{cs.get_redused_levels[data]:.3f}'
                cs_redused_point = pt.add_point(cs_chainage_point, self.__detail_line_gap)
                cs_redused = self.__msp.add_text(text=cs_redused_text, height=self.__drawing_text_height, rotation=90.0, dxfattribs={'layer': self.__layer_normal_text}).set_placement(cs_redused_point)

                # Height line
                cs_diduct_height: float = cs.get_redused_levels[data] - cs_tbm
                h_line_start = pt.add_point(drawing_base, pt.point(pt.scale(value=cs.get_offsets[data], scale=h_scale), 0.0))
                h_line_end = pt.add_point(h_line_start, pt.point(0.0, pt.scale(value=cs_diduct_height, scale=v_scale)))
                h_line = self.__msp.add_line(start=h_line_start, end=h_line_end, dxfattribs={'layer': self.__layer_height_line})

                # Add ground points
                cs_grounds.append(h_line_end)
            
            # Draw ground points
            cs_ground_line = self.__msp.add_polyline2d(points=cs_grounds, dxfattribs={'layer': self.__layer_ground_line})

            new_base = pt.add_point(line_01_end, self.__drawing_gap)
        
        return new_base
    
    # Draw drawings
    def draw(self, drawing_type: str, ls_data: list=[], cs_data: list=[], ls_base=(0.0, 0.0), css_base=(0.0, 0.0), ls_tbm: float=None, css_tbm: float=None, ls_v_scale: int=100, ls_h_scale: int=1000, css_v_scale: int=100, css_h_scale: int=100, ls_title: str=''):
        # If drawing_type is LS_AND_CSS
        if (drawing_type == DrawingManager.LS_AND_CSS):
            # Draw LS
            ls_last_point: tuple = self.__draw_ls(ls_data=ls_data, base_point=ls_base, v_scale=ls_v_scale, h_scale=ls_h_scale, tbm=ls_tbm, title=ls_title)
            # Draw CSS
            cs_las_point: tuple = self.__draw_css(css_data=cs_data, base_point=ls_last_point, v_scale=css_v_scale, h_scale=css_h_scale, tbm=css_tbm)
            # Save Drawing
            self.__doc.saveas('test.dxf')

        # If drawing_type is LS
        elif (drawing_type == DrawingManager.LS):
            # Draw LS
            ls_last_point: tuple = self.__draw_ls(ls_data=ls_data, base_point=ls_base, v_scale=ls_v_scale, h_scale=ls_h_scale, tbm=ls_tbm, title=ls_title)
            # Save Drawing
            self.__doc.saveas('test.dxf')
        
        # If drawing_type is CSS
        elif (drawing_type == DrawingManager.CSS):
            # Draw CSS
            cs_las_point: tuple = self.__draw_css(css_data=cs_data, base_point=css_base, v_scale=css_v_scale, h_scale=css_h_scale, tbm=css_tbm)
            # Save Drawing
            self.__doc.saveas('test.dxf')
        