
from fuiDataStructures.fuiMatrix import fuiMatrix

class fuiFillStyle:
    fmt = "<3I" + fuiMatrix.fmt.strip("<")

    def __init__(self, unkn_0x0:int, color:int, unkn_0x8:int, matrix:fuiMatrix):
        self.fillStyle:dict = {
            "unk_0x0" : unkn_0x0,
            "color" : color,
            "unk_0x8" : unkn_0x8,
            "matrix" : matrix,
        }

    def get(self) -> dict:
        return self.fillStyle

    def __str__(self) -> str:
        return self.fillStyle.__str__()

    def __repr__(self) -> str:
        return self.fillStyle.__repr__()