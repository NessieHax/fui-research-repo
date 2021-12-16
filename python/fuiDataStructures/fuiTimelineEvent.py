from dataclasses import dataclass, field
# from typing import overload
import struct

from fuiDataStructures.fuiMatrix import fuiMatrix
from fuiDataStructures.fuiColorTransform import fuiColorTransform

@dataclass(init=False)
class fuiTimelineEvent:
    fmt = "<6h6f8fI"

    unkn_0x0:int = field(default_factory=int)
    unkn_0x2:int = field(default_factory=int)
    unkn_0x4:int = field(default_factory=int)
    unkn_0x6:int = field(default_factory=int)
    unkn_0x8:int = field(default_factory=int)
    unkn_0xa:int = field(default_factory=int)
    matrix:fuiMatrix = field(repr=False)
    ColorTransform:fuiColorTransform = field(repr=False)
    color:int = field(default_factory=int)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.unkn_0x0 = data[0]
        self.unkn_0x2 = data[1]
        self.unkn_0x4 = data[2]
        self.unkn_0x6 = data[3]
        self.unkn_0x8 = data[4]
        self.unkn_0xa = data[5]
        self.matrix = fuiMatrix(data[6], data[7], data[8], data[9], data[10], data[11])
        self.ColorTransform = fuiColorTransform(data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19])
        self.color = data[20]