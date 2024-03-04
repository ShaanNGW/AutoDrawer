# Import Libraries
# Import points
from .point import Point as pt

# LS class -> Class
class LS:

    # Class constructor -> Method
    def __init__(self, chainage: float, redused_level: float, description: str) -> None:

        # Properties
        self.__chainage: float = chainage
        self.__reduced_level: float = redused_level
        self.__description: str = description

    # Getters and setter
    # Chainage
    @property
    def get_chainage(self) -> float:
        return self.__chainage
    
    # Redused level
    @property
    def get_reduced(self) -> float:
        return self.__reduced_level
    
    # Description
    @property
    def get_description(self) -> float:
        return self.__description
    
    # Class ststic methods
    # Get max chainage -> Method
    @staticmethod
    def get_max_chainage(ls_list: list) -> float:
        # Temparary chainage
        temp_chain: list[float] = []
        
        for ls in ls_list:
            temp_chain.append(ls.get_chainage)
        
        # Return max chainage
        return max(temp_chain)
    
    @staticmethod
    def get_max_redused(ls_list: list) -> float:
        # Temparary redused
        temp_redused: list[float] = []
        
        for ls in ls_list:
            temp_redused.append(ls.get_reduced)
        
        # Return max chainage
        return max(temp_redused)
    
    @staticmethod
    def get_tbm(ls_list: list) -> float:
        # Temparary redused
        temp_redused: list[float] = []
        
        for ls in ls_list:
            temp_redused.append(ls.get_reduced)

        min_redused = min(temp_redused)

        # Return max chainage
        return (round(min_redused - pt.to_meter(value=5.0, unit=pt.M)))
    
    
    # Class display name -> Method
    def __repr__(self) -> str:
        return f'LS(chainage={self.__chainage}, redused={self.__reduced_level}, description={self.__description})'