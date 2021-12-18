from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiRect import fuiRect

@dataclass(init=False)
class fuiEdittext:
    fmt = "<i4fifI6i256s"

    unkn_0x0:int = field(default_factory=int)
    rect:fuiRect = field(default_factory=fuiRect)
    unkn_0x14:int = field(default_factory=int)
    unkn_0x18:float = field(default_factory=float)
    color:int = field(default_factory=int)
    unkn_0x20:int = field(default_factory=int)
    unkn_0x24:int = field(default_factory=int)
    unkn_0x28:int = field(default_factory=int)
    unkn_0x2c:int = field(default_factory=int)
    unkn_0x30:int = field(default_factory=int)
    unkn_0x34:int = field(default_factory=int)
    html_str:str = field(default_factory=str)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.unkn_0x0 = data[0]
        self.rect = fuiRect(data[1], data[2], data[3], data[4])
        self.unkn_0x14 = data[5]
        self.unkn_0x18 = data[6]
        self.color = data[7]
        self.unkn_0x20 = data[8]
        self.unkn_0x24 = data[9]
        self.unkn_0x28 = data[10]
        self.unkn_0x2c = data[11]
        self.unkn_0x30 = data[12]
        self.unkn_0x34 = data[13]
        self.html_str = data[14]
