from dataclasses import dataclass
import struct

from fuiDataStructures.fuiObject import fuiObject

@dataclass(init=False)
class fuiVert(fuiObject):
    fmt = "<2f"

    x:float
    y:float

    def __init__(self, raw_bytes:bytes):
        self.x, self.y = struct.unpack(self.fmt, raw_bytes)

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.x, self.y)