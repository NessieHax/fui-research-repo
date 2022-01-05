from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiMatrix import fuiMatrix
from fuiDataStructures.fuiColorTransform import fuiColorTransform

@dataclass(init=False)
class fuiTimelineEvent:
    fmt = f"<4b4h{fuiMatrix.fmt}{fuiColorTransform.fmt}I"

    event_type:int = field(default_factory=int)
    unkn_0x1:int = field(default_factory=int)
    obj_type:int = field(default_factory=int)
    unkn_0x3:int = field(default_factory=int)
    unkn_0x4:int = field(default_factory=int)
    index:int = field(default_factory=int)
    unkn_0x8:int = field(default_factory=int)
    name_index:int = field(default_factory=int)
    matrix:fuiMatrix = field(default_factory=fuiMatrix)
    ColorTransform:fuiColorTransform = field(default_factory=fuiColorTransform)
    color:int = field(default_factory=int)

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

    def pack(self) -> bytearray:
        data = struct.pack(self.fmt, self.event_type, self.unkn_0x1, self.obj_type, self.unkn_0x3, self.unkn_0x4, self.index, self.unkn_0x8, self.name_index,
         *self.matrix, *self.ColorTransform, self.color)
        return bytearray(data)