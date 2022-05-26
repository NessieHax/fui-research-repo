import struct
from dataclasses import dataclass, field

from fuiDataStructures.fuiObject import fuiObject

@dataclass(init=False)
class fuiTimelineFrame(fuiObject):
    fmt = "<64s2i"
    size = struct.calcsize(fmt)

    frame_name:str
    event_index:int
    event_count:int

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.frame_name = data[0].decode('UTF-8').strip("\0")
        self.event_index = data[1]
        self.event_count = data[2]

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.frame_name.encode("UTF-8"), self.event_index, self.event_count)