from dataclasses import dataclass, field
import struct

@dataclass(init=False)
class fuiFontName:
    fmt = "<i64si64s2i64s2i44s"

    unkn_0x0:int = field(default_factory=int)
    font_name:str = field(default_factory=str)
    unkn_0x44:int = field(default_factory=int)
    unkn_str0:str = field(default_factory=str)
    unkn_0x88:int = field(default_factory=int)
    unkn_0x8c:int = field(default_factory=int)
    unkn_str1:str = field(default_factory=str)
    unkn_0xd0:int = field(default_factory=int)
    unkn_0xd4:int = field(default_factory=int)
    unkn_str2:str = field(default_factory=str)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.unkn_0x0 = data[0]
        self.font_name = data[1].decode('UTF-8').strip("\0")
        self.unkn_0x44 = data[2]
        self.unkn_str0 = data[3].decode('UTF-8').strip("\0")
        self.unkn_0x88 = data[4]
        self.unkn_0x8c = data[5]
        self.unkn_str1 = data[6].decode('UTF-8').strip("\0")
        self.unkn_0xd0 = data[7]
        self.unkn_0xd4 = data[8]
        self.unkn_str2 = data[9].decode('UTF-8').strip("\0")