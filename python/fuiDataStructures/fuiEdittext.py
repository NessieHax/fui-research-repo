from dataclasses import dataclass, field
import struct, re

from fuiDataStructures.fuiRect import fuiRect

@dataclass(init=False)
class fuiEdittext:
    fmt = "<i4fifIb3x3if4?256s"

    unkn_0x0:int = field(default_factory=int) #! unused!
    rect:fuiRect = field(default_factory=fuiRect)
    font_id:int = field(default_factory=int)
    unkn_0x18:float = field(default_factory=float)
    color:int = field(default_factory=int)
    unkn_0x20:int = field(default_factory=int) #! alignment stuff 1 byte
    unkn_0x24:int = field(default_factory=int)
    unkn_0x28:int = field(default_factory=int)
    unkn_0x2c:int = field(default_factory=int)
    unkn_0x30:float = field(default_factory=float) #! unused ?
    unkn_0x34:bool = field(default_factory=bool) #! bool flag
    unkn_0x35:bool = field(default_factory=bool) #! bool flag
    unkn_0x36:bool = field(default_factory=bool) #! bool flag unused!
    unkn_0x37:bool = field(default_factory=bool) #! bool flag unused!
    html_str:str = field(default_factory=str)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.unkn_0x0 = data[0]
        self.rect = fuiRect(data[1], data[2], data[3], data[4])
        self.font_id = data[5]
        self.unkn_0x18 = data[6]
        self.color = data[7]
        self.unkn_0x20 = data[8]
        self.unkn_0x24 = data[9]
        self.unkn_0x28 = data[10]
        self.unkn_0x2c = data[11]
        self.unkn_0x30 = data[12]
        self.unkn_0x34 = data[13]
        self.unkn_0x35 = data[14]
        self.unkn_0x36 = data[15]
        self.unkn_0x37 = data[16]
        self.html_str = data[17].decode('UTF-8', "ignore")