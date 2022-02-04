from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiObject import fuiObject
from fuiDataStructures.fuiRect import fuiRect

@dataclass(init=False)
class fuiShape(fuiObject):
    fmt = "<3i4f"

    unk_0x0:int = field(default_factory=int)
    component_index:int = field(default_factory=int)
    component_count:int = field(default_factory=int)
    area:fuiRect = field(default_factory=fuiRect)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.unk_0x0 = data[0]
        self.component_index = data[1]
        self.component_count = data[2]
        self.area = fuiRect(data[3], data[4], data[5], data[6])

    def pack(self) -> bytearray:
        return bytearray(struct.pack(self.fmt, self.unk_0x0, self.component_index, self.component_count, *self.area))