from dataclasses import dataclass, field
import struct

@dataclass(init=False)
class fuiTimelineFrame:
    fmt = "<64s2i"

    frame_name:str = field(default_factory=str)
    event_index:int = field(default_factory=int)
    event_count:int = field(default_factory=int)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.frame_name = data[0].decode('UTF-8').strip("\0")
        self.event_index = data[1]
        self.event_count = data[2]

    def pack(self) -> bytearray:
        return bytearray(struct.pack(self.fmt, self.frame_name.encode("UTF-8"), self.event_index, self.event_count))