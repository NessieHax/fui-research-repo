from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiObject import fuiObject
from fuiDataStructures.fuiMatrix import fuiMatrix
from fuiDataStructures.fuiColorTransform import fuiColorTransform

@dataclass(init=False)
class fuiTimelineEvent(fuiObject):
    fmt = f"<4b4h{fuiMatrix.fmt}{fuiColorTransform.fmt}I"
    size = struct.calcsize(fmt)

    event_type:int
    unkn_0x1:int
    obj_type:int
    unkn_0x3:int
    unkn_0x4:int
    index:int
    unkn_0x8:int
    name_index:int
    matrix:fuiMatrix = field(default_factory=fuiMatrix, repr=False)
    ColorTransform:fuiColorTransform = field(default_factory=fuiColorTransform, repr=False)
    color:int = field(repr=False)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.event_type = data[0]
        self.unkn_0x1 = data[1]
        self.obj_type = data[2]
        self.unkn_0x3 = data[3]
        self.unkn_0x4 = data[4]
        self.index = data[5]
        self.unkn_0x8 = data[6]
        self.name_index = data[7]
        self.matrix = fuiMatrix(data[8], data[9], data[10], data[11], data[12], data[13])
        self.ColorTransform = fuiColorTransform(data[14], data[15], data[16], data[17], data[18], data[19], data[20], data[21])
        self.color = data[22]

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.event_type, self.unkn_0x1, self.obj_type, self.unkn_0x3, self.unkn_0x4, self.index, self.unkn_0x8, self.name_index,
         *self.matrix, *self.ColorTransform, self.color)
        