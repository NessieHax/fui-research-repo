from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiMatrix import fuiMatrix
@dataclass(init=False)
class fuiFillStyle:
    fmt = "3I" + fuiMatrix.fmt

    unkn_0x0:int = field(default_factory=int)
    color:int = field(default_factory=int)
    bitmap_index:int = field(default_factory=int)
    matrix:fuiMatrix = field(default_factory=fuiMatrix)

    def __init__(self, unkn_0x0:int, color:int, bitmap_index:int, matrix:fuiMatrix):
        self.unkn_0x0 = unkn_0x0 #! 1 == fillWithColor | 5 == use bitmap | 3 == scale bitmap by matrix ??
        self.color = color
        self.bitmap_index = bitmap_index
        self.matrix = matrix

    def __iter__(self):
        return iter([self.unkn_0x0, self.color, self.bitmap_index, *self.matrix])