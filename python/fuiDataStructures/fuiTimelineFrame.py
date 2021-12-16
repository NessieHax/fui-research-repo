from dataclasses import dataclass, field
import struct

@dataclass(init=False)
class fuiTimelineFrame:
    fmt = "<64s2i"

    frame_name:str = field(default_factory=str)
    unkn_0x40:int = field(default_factory=int)
    unkn_0x44:int = field(default_factory=int)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.frame_name = data[0].decode('UTF-8').strip("\0")
        self.unkn_0x40 = data[1]
        self.unkn_0x44 = data[2]