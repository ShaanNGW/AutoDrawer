# Import libraries
from .point import Point as pt

# CSS class -> Class
class CSS:

    # Class constructor -> Method
    def __init__(self, chainage: float, offsets: list[float], redused_levels: list[float], descriptions: list[str]) -> None:

        # Properties
        # Chainage
        self.__chainage: float = chainage

        # Sort and set values
        self.__offsets, self.__redused_levels, self.__descriptions = self.__sort_list(offset=offsets, reduced_level=redused_levels, description=descriptions)
    
    # Getters and setters
    # Chainage
    @property
    def get_chainage(self) -> float:
        return self.__chainage
    
    # Offsets
    @property
    def get_offsets(self) -> list[float]:
        return self.__offsets
    
    # Redused levels
    @property
    def get_redused_levels(self) -> list[float]:
        return self.__redused_levels
    
    # Descriptions
    @property
    def get_descriptions(self) -> list[str]:
        return self.__descriptions
    
    # Get offset width
    def get_offset_width(self):
        # Width
        width: float = 0.0

        width = abs(min(self.__offsets)) + abs(max(self.__offsets))
        
        # Return value
        return width

    # Get max redused
    @staticmethod
    def get_tbm(css_data: list):
        temp_redused: list[float] = []

        for cs in css_data:
            temp_redused.append(min(cs.get_redused_levels))
        
        min_redused =  min(temp_redused)

        return round(min_redused - pt.to_meter(value=5.0, unit=pt.M))

    # Static Methods
    # List sort
    @staticmethod
    def __sort_list(offset: list[float], reduced_level: list[float], description: list[str]):
        
        # Temp dictionary
        temp_dic: dict = {}

        # Add data to dictionary
        for data in range(len(offset)):
            # Add data to temp_dic
            temp_dic[offset[data]] = [reduced_level[data], description[data]]
        
        # Sort temp_dic
        new_dic: dict = dict(sorted(temp_dic.items()))

        # Return new data
        temp_offset: list[float] = []
        temp_reduced: list[float] = []
        temp_description: list[float] = []

        for key in new_dic.keys():
            temp_offset.append(key)
            temp_reduced.append(new_dic[key][0])
            temp_description.append(new_dic[key][1])
        
        return temp_offset, temp_reduced, temp_description

    # Class diplayer
    def __repr__(self) -> str:
        return f'CSS(chainage={self.__chainage}, offsets={self.__offsets}, redused={self.__redused_levels}, description={self.__descriptions})'