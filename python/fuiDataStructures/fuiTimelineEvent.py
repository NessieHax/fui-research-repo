from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiMatrix import fuiMatrix
from fuiDataStructures.fuiColorTransform import fuiColorTransform

@dataclass(init=False)
class fuiTimelineEvent:
    fmt = "<6h6f8fI"

    event_type:int = field(default_factory=int)
    obj_type:int = field(default_factory=int)
    unkn_0x4:int = field(default_factory=int)
    index:int = field(default_factory=int)
    unkn_0x8:int = field(default_factory=int)
    name_index:int = field(default_factory=int)
    matrix:fuiMatrix = field(default_factory=fuiMatrix, repr=False)
    ColorTransform:fuiColorTransform = field(default_factory=fuiColorTransform, repr=False)
    color:int = field(default_factory=int, repr=False)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.event_type = data[0]
        self.obj_type = data[1]
        self.unkn_0x4 = data[2]
        self.index = data[3]
        self.unkn_0x8 = data[4]
        self.name_index = data[5]
        self.matrix = fuiMatrix(data[6], data[7], data[8], data[9], data[10], data[11])
        self.ColorTransform = fuiColorTransform(data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19])
        self.color = data[20]