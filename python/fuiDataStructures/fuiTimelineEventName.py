from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiObject import fuiObject

@dataclass(init=False)
class fuiTimelineEventName(fuiObject):
    fmt = "<64s"
    size = struct.calcsize(fmt)

    name:str

    def __init__(self, raw_bytes:bytes):
        self.name = struct.unpack(self.fmt, raw_bytes)[0].decode('UTF-8').strip("\0")

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.name.encode('UTF-8'))