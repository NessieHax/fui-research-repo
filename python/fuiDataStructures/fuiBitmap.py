from dataclasses import dataclass, field
import struct

@dataclass(init=False)
class fuiBitmap:
    fmt = "<8i"

    unkn_0x0:int = field(default_factory=int)
    obj_type:int = field(default_factory=int)
    scale_width:int = field(default_factory=int)
    scale_height:int = field(default_factory=int)
    offset:int = field(default_factory=int)
    size:int = field(default_factory=int)
    unkn_0x18:int = field(default_factory=int)
    unkn_0x1c:int = field(default_factory=int)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.unkn_0x0 = data[0]
        self.obj_type = data[1]
        self.scale_width = data[2]
        self.scale_height = data[3]
        self.offset = data[4]
        self.size = data[5]
        self.unkn_0x18 = data[6]
        self.unkn_0x1c = data[7]