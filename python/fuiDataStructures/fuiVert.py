from dataclasses import dataclass, field
import struct

@dataclass(init=False)
class fuiVert:
    x:float = field(default_factory=float)
    y:float = field(default_factory=float)

    def __init__(self, raw_bytes:bytes):
        self.x, self.y = struct.unpack(self.fmt, raw_bytes)
    
    @property
    def fmt(self) -> str:
        return "<2f"