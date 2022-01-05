from dataclasses import dataclass, field
import struct

@dataclass(init=False)
class fuiTimelineEventName:
    fmt = "<64s"

    name:str = field(default_factory=str)

    def __init__(self, raw_bytes:bytes):
        self.name = struct.unpack(self.fmt, raw_bytes)[0].decode('UTF-8').strip("\0")

    def pack(self) -> bytearray:
        return bytearray(struct.pack(self.fmt, self.name.encode('UTF-8')))