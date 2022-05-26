from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiObject import fuiObject

@dataclass(init=False)
class fuiFontName(fuiObject):
    fmt = "<i64s192x"
    size = struct.calcsize(fmt)

    id:int
    name:str

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.id = data[0]
        self.name = data[1].decode('UTF-8').strip("\0")

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.id, self.name.encode('UTF-8'))