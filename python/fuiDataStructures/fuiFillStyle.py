from dataclasses import dataclass, field

from fuiDataStructures.fuiMatrix import fuiMatrix
@dataclass
class fuiFillStyle:
    fmt = "3I" + fuiMatrix.fmt

    class eFuiFillType:
        pass

    fillType:int = field(default_factory=int) #! eFuiFillType : 1 == fillWithColor | 5 == use bitmap | 3 == scale bitmap by matrix ??
    color:int = field(default_factory=int)
    bitmap_index:int = field(default_factory=int)
    matrix:fuiMatrix = field(default_factory=fuiMatrix)

    def __iter__(self):
        return iter([self.fillType, self.color, self.bitmap_index, *self.matrix])