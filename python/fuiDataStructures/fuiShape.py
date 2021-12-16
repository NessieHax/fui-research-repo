from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiRect import fuiRect

@dataclass(init=False)
class fuiShape:
    fmt = "<3i4f"

    unk_0x0:int = field(default_factory=int)
    unk_0x4:int = field(default_factory=int)
    obj_type:int = field(default_factory=int)
    rect:fuiRect = field(default_factory=fuiRect)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.unk_0x0 = data[0]
        self.unk_0x4 = data[1]
        self.obj_type = data[2]
        self.rect = fuiRect(data[3], data[4], data[5], data[6])