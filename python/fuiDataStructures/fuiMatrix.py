

class fuiMatrix:
    fmt = "<6f"

    def __init__(self, scale_x:float, scale_y:float, rotate_skew0:float, rotate_skew1:float, translae_x:float, translae_y:float):
        self.matrix:dict = {
            "Scale" : (scale_x, scale_y),
            "Ratate_skew" : (rotate_skew0, rotate_skew1),
            "Tranlate" : (translae_x, translae_y)
        }

    def get(self) -> dict:
        return self.matrix

    def __str__(self) -> str:
        return self.matrix.__str__()

    def __repr__(self) -> str:
        return self.matrix.__repr__()