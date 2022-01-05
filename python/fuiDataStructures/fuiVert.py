from dataclasses import dataclass, field
import struct

@dataclass(init=False)
class fuiVert:
    fmt = "<2f"

    x:float = field(default_factory=float)
    y:float = field(default_factory=float)

    def __init__(self, raw_bytes:bytes):
        self.x, self.y = struct.unpack(self.fmt, raw_bytes)

    def pack(self) -> bytearray:
        return bytearray(struct.pack(self.fmt, self.x, self.y))