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

    # Colors
    BLACK = colors.RGB(r=0, g=0, b=0)
    WHITE = colors.RGB(r=225, g=225, b=225)
    RED = colors.RGB(r=225, g=0, b=0)
    YELLOW = colors.RGB(r=255, g=255, b=0)
    BLUE = colors.RGB(r=0, g=0, b=255)
    GREEN = colors.RGB(r=0, g=255, b=0)
    CYEN = colors.RGB(r=0, g=255, b=255)
    PINK = colors.RGB(r=255, g=105, b=180)

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
        # Set work space
        self.__msp = self.__doc.modelspace()
    
    # Draw ls -> Method
    def draw_ls(self, ls_data: list, base_point=pt.point(0.0, 0.0), v_scale: int=100, h_scale: int=1000, tbm: float=None, title: str='') -> tuple:

        # If tbm is None
        if (tbm == None):
            ls_tbm: float = LS.get_tbm(ls_list=ls_data)
        # If not
        else:
            ls_tbm: float = tbm
        
        # Line 01
        line_01_start: pt.point = base_point
        line_01_end: pt.point = pt.add_point(line_01_start, self.__detail_line_width, pt.point(pt.scale(value=LS.get_max_chainage(ls_list=ls_data), scale=h_scale), 0.0), self.__extra_line_width)
        line_01 = self.__msp.add_line(start=line_01_start, end=line_01_end)

        # Line 01 Text
        line_01_txt_str: str = 'Chainage (m)'
        line_01_txt_point = pt.add_point(line_01_start, self.__text_gap)
        line_01_txt = self.__msp.add_text(text=line_01_txt_str, height=self.__drawing_text_height).set_placement(line_01_txt_point)

        # Line 02
        line_02_start = pt.add_point(line_01_start, self.__detail_line_gap)
        line_02_end = pt.add_point(line_01_end, self.__detail_line_gap)
        line_02 = self.__msp.add_line(start=line_02_start, end=line_02_end)

        # Line 02 Text
        line_02_txt_str: str = 'Redused Level (m)'
        line_02_txt_point = pt.add_point(line_02_start, self.__text_gap)
        line_02_txt = self.__msp.add_text(text=line_02_txt_str, height=self.__drawing_text_height).set_placement(line_02_txt_point)

        # Line 03
        line_03_start = pt.add_point(line_02_start, self.__detail_line_gap)
        line_03_end = pt.add_point(line_02_end, self.__detail_line_gap)
        line_03 = self.__msp.add_line(start=line_03_start, end=line_03_end)
        
        # Line 03 Text
        line_03_txt_str: str = f'TBM: {ls_tbm:.2f}m'
        line_03_txt_point = pt.add_point(line_03_start, self.__text_gap)
        line_03_txt = self.__msp.add_text(text=line_03_txt_str, height=self.__drawing_text_height).set_placement(line_03_txt_point)

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
            chainage = self.__msp.add_text(text=chainage_text, height=self.__drawing_text_height, rotation=90.0).set_placement(chainage_point)

            # Set Redused
            redused_text: str = f'{ls.get_reduced:.3f}'
            redused_point = pt.add_point(temp_base, pt.point(pt.scale(value=ls.get_chainage, scale=h_scale), 0.0), pt.point((self.__drawing_text_height/2), 0.0), self.__text_gap, self.__detail_line_gap)
            redused = self.__msp.add_text(text=redused_text, height=self.__drawing_text_height, rotation=90.0).set_placement(redused_point)

            # Diduct redused
            diduct_redused = pt.scale(value=ls.get_reduced, scale=v_scale) - pt.scale(value=ls_tbm, scale=v_scale)

            # Set lines
            line_start = pt.add_point(temp_drawing_base, pt.point(pt.scale(value=ls.get_chainage, scale=h_scale), 0.0))
            line_end = pt.add_point(line_start, pt.point(0.0, diduct_redused))
            line = self.__msp.add_line(start=line_start, end=line_end)

            # Description Line
            des_line_start = line_end
            des_line_end = pt.add_point(line_start, pt.point(0.0, (max_redused + pt.to_meter(value=50.0, unit=pt.MM))))
            des_line = self.__msp.add_line(start=des_line_start, end=des_line_end)

            # Set description
            des_txt_str: str = ls.get_description
            des_txt_point = pt.add_point(des_line_end, self.__text_gap)
            des_txt = self.__msp.add_text(text=des_txt_str, height=self.__drawing_text_height, rotation=45.0).set_placement(des_txt_point)
            
            # Add end point to list
            temp_ground.append(line_end)
        
        # Draw ground
        ground = self.__msp.add_polyline2d(points=temp_ground)

        # Set title
        title_text_str: str = f'LS of {title}'
        title_text_point = pt.add_point(pt.center(start=line_01_start, end=line_01_end), pt.point(0.0, -pt.to_meter(value=20.0, unit=pt.MM)))
        title_text = self.__msp.add_text(text=title_text_str, height=self.__text_title_height).set_placement(title_text_point, align=TextEntityAlignment.MIDDLE)

        # Set Scale Horizontal
        h_scale_text_str: str = f'Horizontal Scale 1:{h_scale}'
        h_scale_text_point = pt.add_point(line_01_end, pt.point(0.0, -pt.to_meter(value=10.0, unit=pt.MM)), pt.point(0.0, -pt.to_meter(value=20.0, unit=pt.MM)))
        h_scale_text = self.__msp.add_text(text=h_scale_text_str, height=self.__drawing_text_height).set_placement(h_scale_text_point, align=TextEntityAlignment.RIGHT)
        
        # Set Scale Horizontal
        v_scale_text_str: str = f'Vertical Scale 1:{v_scale}'
        v_scale_text_point = pt.add_point(h_scale_text_point, pt.point(0.0, -pt.to_meter(value=5.0, unit=pt.MM)))
        v_scale_text = self.__msp.add_text(text=v_scale_text_str, height=self.__drawing_text_height).set_placement(v_scale_text_point, align=TextEntityAlignment.RIGHT)

        return line_01_end
    
    # Draw ls -> Method
    def draw_css(self, css_data: list, base_point=pt.point(0.0, 0.0), v_scale: int=100, h_scale: int=100, tbm: float=None):
        
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
            line_01 = self.__msp.add_line(start=line_01_start, end=line_01_end)

            # Line 01 Text
            line_01_txt_str: str = 'Chainage (m)'
            line_01_txt_point = pt.add_point(line_01_start, self.__text_gap)
            line_01_txt = self.__msp.add_text(text=line_01_txt_str, height=self.__drawing_text_height).set_placement(line_01_txt_point)

            # Line 02
            line_02_start = pt.add_point(line_01_start, self.__detail_line_gap)
            line_02_end = pt.add_point(line_01_end, self.__detail_line_gap)
            line_02 = self.__msp.add_line(start=line_02_start, end=line_02_end)

            # Line 02 Text
            line_02_txt_str: str = 'Redused Level (m)'
            line_02_txt_point = pt.add_point(line_02_start, self.__text_gap)
            line_02_txt = self.__msp.add_text(text=line_02_txt_str, height=self.__drawing_text_height).set_placement(line_02_txt_point)

            # Line 03
            line_03_start = pt.add_point(line_02_start, self.__detail_line_gap)
            line_03_end = pt.add_point(line_02_end, self.__detail_line_gap)
            line_03 = self.__msp.add_line(start=line_03_start, end=line_03_end)
            
            # Line 03 Text
            line_03_txt_str: str = f'TBM: {cs_tbm:.2f}m'
            line_03_txt_point = pt.add_point(line_03_start, self.__text_gap)
            line_03_txt = self.__msp.add_text(text=line_03_txt_str, height=self.__drawing_text_height).set_placement(line_03_txt_point)

            # Set title
            cs_title_text_str: str = f'{cs.get_chainage:.3f}m'
            cs_title_text_point = pt.add_point(new_base, pt.center(start=line_01_start, end=line_01_end), pt.point(0.0, -pt.to_meter(value=20.0, unit=pt.MM)))
            cs_title_text = self.__msp.add_text(text=cs_title_text_str, height=self.__text_title_height).set_placement(cs_title_text_point, align=TextEntityAlignment.MIDDLE)

            # Set Scale Horizontal
            h_scale_text_str: str = f'Horizontal Scale 1:{h_scale}'
            h_scale_text_point = pt.add_point(line_01_end, pt.point(0.0, -pt.to_meter(value=10.0, unit=pt.MM)), pt.point(0.0, -pt.to_meter(value=20.0, unit=pt.MM)))
            h_scale_text = self.__msp.add_text(text=h_scale_text_str, height=self.__drawing_text_height).set_placement(h_scale_text_point, align=TextEntityAlignment.RIGHT)
            
            # Set Scale Horizontal
            v_scale_text_str: str = f'Vertical Scale 1:{v_scale}'
            v_scale_text_point = pt.add_point(h_scale_text_point, pt.point(0.0, -pt.to_meter(value=5.0, unit=pt.MM)))
            v_scale_text = self.__msp.add_text(text=v_scale_text_str, height=self.__drawing_text_height).set_placement(v_scale_text_point, align=TextEntityAlignment.RIGHT)

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
                cs_chainage = self.__msp.add_text(text=cs_chainage_text, height=self.__drawing_text_height, rotation=90.0).set_placement(cs_chainage_point)

                # Set Redused
                cs_redused_text: str = f'{cs.get_redused_levels[data]:.3f}'
                cs_redused_point = pt.add_point(cs_chainage_point, self.__detail_line_gap)
                cs_redused = self.__msp.add_text(text=cs_redused_text, height=self.__drawing_text_height, rotation=90.0).set_placement(cs_redused_point)

                # Height line
                cs_diduct_height: float = cs.get_redused_levels[data] - cs_tbm
                h_line_start = pt.add_point(drawing_base, pt.point(pt.scale(value=cs.get_offsets[data], scale=h_scale), 0.0))
                h_line_end = pt.add_point(h_line_start, pt.point(0.0, pt.scale(value=cs_diduct_height, scale=v_scale)))
                h_line = self.__msp.add_line(start=h_line_start, end=h_line_end)

                # Add ground points
                cs_grounds.append(h_line_end)
            
            # Draw ground points
            cs_ground_line = self.__msp.add_polyline2d(points=cs_grounds)

            

            new_base = pt.add_point(line_01_end, self.__drawing_gap)

            

        self.__doc.saveas('test.dxf')