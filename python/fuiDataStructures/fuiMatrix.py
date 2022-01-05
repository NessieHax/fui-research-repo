from dataclasses import dataclass, field

@dataclass(init=False)
class fuiMatrix:
    fmt = "6f"

    scale:tuple = field(default_factory=tuple)
    rotate_skrew:tuple = field(default_factory=tuple)
    translate:tuple = field(default_factory=tuple)

    def __init__(self, scale_x:float, scale_y:float, rotate_skew0:float, rotate_skew1:float, translate_x:float, translate_y:float):
        self.scale = (scale_x, scale_y)
        self.rotate_skrew = (rotate_skew0, rotate_skew1)
        self.translate = (translate_x, translate_y)

    def __iter__(self):
        return iter([*self.scale, *self.rotate_skrew, *self.translate])