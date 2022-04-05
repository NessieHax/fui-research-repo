from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiObject import fuiObject
from fuiDataStructures.fuiMatrix import fuiMatrix
from fuiDataStructures.fuiFillStyle import fuiFillStyle

@dataclass(init=False)
class fuiShapeComponent(fuiObject):
    fmt = f"<{fuiFillStyle.fmt}2i"

    fillInfo:fuiFillStyle = field(default_factory=fuiFillStyle)
    vert_index:int
    vert_count:int

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.fillInfo = fuiFillStyle(data[0], data[1], data[2], fuiMatrix(data[3], data[4], data[5], data[6], data[7], data[8]))
        self.vert_index = data[9]
        self.vert_count = data[10]

    def pack(self) -> bytes:
        return struct.pack(self.fmt, *self.fillInfo, self.vert_index, self.vert_count)