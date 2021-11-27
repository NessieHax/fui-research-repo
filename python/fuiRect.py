

class fuiRect:
    def __init__(self, x:float, y:float, width:float, height:float):
        self.rect:dict = {
            "x" : x,
            "width" : width,
            "y" : y,
            "height" : height
           }

    def get() -> dict:
        return self.rect

    def __str__(self):
        return self.rect.__str__()