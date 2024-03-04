# Import libraries

# Point class -> Class
class Point:

    # Class lirarals
    MM: float = 'mm'
    CM: float = 'cm'
    M: float = 'm'

    # Point
    @staticmethod
    def point(x: float, y: float):
        return (x, y)

    # Scaler -> Method
    @staticmethod
    def scale(value: float, scale: int) -> float:
        # Return scaled value
        return ((1 / scale) * value)

    # To meter converter -> Method
    @staticmethod
    def to_meter(value: float, unit: str) -> float:
        # If unit is mm
        if (unit == 'mm'):
            return (value / 1000)
        
        # If unit is cm
        elif (unit == 'cm'):
            return (value / 100)
        
        # If unit m
        elif (unit == 'm'):
            return value

    # Add points -> Method
    @staticmethod
    def add_point(*arg) -> float:
        x: float = 0.0
        y: float = 0.0

        for data in arg:
            x += data[0]
            y += data[1]
        
        return (x, y)

    # Get center point
    def center(start, end):
        x = end[0] - start[0]
        y = end[1] - start[1]

        return (x/2, y/2)