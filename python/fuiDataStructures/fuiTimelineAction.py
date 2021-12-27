from dataclasses import dataclass, field
import struct

@dataclass(init=False)
class fuiTimelineAction:
    fmt = "<2h64s64s"

    class eAction:
        prev_event = 0 #! links action_arg0 to action_arg1 as the next event(focus)
        next_event = 1 #! links action_arg0 to action_arg1 as the next event(focus)
        cycle = 13

    action_type:int = field(default_factory=int)
    unkn_0x2:int = field(default_factory=int)
    action_arg0:str = field(default_factory=str)
    action_arg1:str = field(default_factory=str)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.action_type = data[0]
        self.unkn_0x2 = data[1]
        self.action_arg0 = data[2].decode('UTF-8').strip("\0")
        self.action_arg1 = data[3].decode('UTF-8').strip("\0")
