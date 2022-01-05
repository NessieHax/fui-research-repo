from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiMatrix import fuiMatrix
@dataclass(init=False)
class fuiFillStyle:
    fmt = "3I" + fuiMatrix.fmt

    unkn_0x0:int = field(default_factory=int)
    color:int = field(default_factory=int)
    unkn_0x8:int = field(default_factory=int)
    matrix:fuiMatrix = field(default_factory=fuiMatrix)

    def __init__(self, unkn_0x0:int, color:int, unkn_0x8:int, matrix:fuiMatrix):
        self.unkn_0x0 = unkn_0x0
        self.color = color
        self.unkn_0x8 = unkn_0x8
        self.matrix = matrix

    def __iter__(self):
        return iter([self.unkn_0x0, self.color, self.unkn_0x8, *self.matrix])