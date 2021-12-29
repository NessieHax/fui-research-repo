from dataclasses import dataclass, field

@dataclass(init=False, repr=False)
class fuiRect:
    x:tuple = field(default_factory=tuple)
    y:tuple = field(default_factory=tuple)

    def __init__(self, min_x:float, max_x:float, min_y:float, max_y:float):
        self.x = (min_x, max_x)
        self.y = (min_y, max_y)

    def get_size(self) -> tuple:
        return (self.get_width(), self.get_height())

    def get_width(self) -> float:
        return self.x[1] - self.x[0]

    def get_height(self) -> float:
        return self.y[1] - self.y[0]

    def set_x(self, min_x:float, max_x:float) -> None:
        self.x = (min_x, max_x)

    def set_y(self, min_y:float, max_y:float) -> None:
        self.y = (min_y, max_y)

    def __repr__(self) -> str:
        return self.get_size().__repr__()

    def __str__(self) -> str:
        return f"{self.x=} {self.y=}"