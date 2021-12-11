
class fuiRect:
    def __init__(self, x_min:float, x_max:float, y_min:float, y_max:float):
        self.__rect:dict = {
            "min_x" : x_min,
            "max_x" : x_max,
            "min_y" : y_min,
            "max_y" : y_max
           }

    def get(self) -> dict:
        return self.__rect

    def get_size(self) -> tuple:
        return (self.get_width(),self.get_height())

    def get_width(self) -> float:
        return self.__rect["max_x"]-self.__rect["min_x"]

    def get_height(self) -> float:
        return self.__rect["max_y"]-self.__rect["min_y"]

    def __str__(self):  
        return self.__rect.__str__()