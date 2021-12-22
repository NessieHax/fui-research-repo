from dataclasses import dataclass, field
import struct

@dataclass(init=False)
class fuiBitmap:
    fmt = "<8i"

    unkn_0x0:int = field(default_factory=int)
    flags:int = field(default_factory=int)
    width:int = field(default_factory=int)
    height:int = field(default_factory=int)
    offset:int = field(default_factory=int)
    size:int = field(default_factory=int)
    zlib_data_offset:int = field(default_factory=int)
    unkn_0x1c:int = field(default_factory=int)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.unkn_0x0 = data[0]
        self.flags = data[1] #! bitmask (1 << 3) == insert zlib alpha channel data
        self.width = data[2]
        self.height = data[3]
        self.offset = data[4]
        self.size = data[5]
        self.zlib_data_offset = data[6] #! zlib compressed size ??
        self.unkn_0x1c = data[7] #! set to -1 if they was an error at runtime