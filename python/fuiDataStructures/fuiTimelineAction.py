from dataclasses import dataclass, field
import struct

@dataclass(init=False)
class fuiTimelineAction:
    fmt = "<2h64s64s"

    unkn_0x0:int = field(default_factory=int)
    unkn_0x2:int = field(default_factory=int)
    action_name:str = field(default_factory=str)
    unk_str:str = field(default_factory=str)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.unkn_0x0 = data[0]
        self.unkn_0x2 = data[1]
        self.action_name = data[2].decode('UTF-8').strip("\0")
        self.unk_str = data[3].decode('UTF-8').strip("\0")
