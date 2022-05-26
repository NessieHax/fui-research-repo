from dataclasses import dataclass, field
import struct, re

from fuiDataStructures.fuiObject import fuiObject
from fuiDataStructures.fuiRect import fuiRect

@dataclass(init=False)
class fuiEdittext(fuiObject):
    fmt = f"<i{fuiRect.fmt}if2i4f2?2x256s"
    size = struct.calcsize(fmt)

    unkn_0x0:int #! probably old Symbol index now unused
    size:fuiRect = field(default_factory=fuiRect)
    font_id:int 
    font_scale:float
    color:int #! fuiRGBA
    alignment:int #! 0 - 3

    #! likely a fuiRect
    unkn_0x24:float
    unkn_0x28:float
    unkn_0x2c:float
    unkn_0x30:float

    unkn_0x34:bool
    unkn_0x35:bool
    
    html_str:bytes = field(repr=False)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.unkn_0x0 = data[0]
        self.size = fuiRect(data[1], data[2], data[3], data[4])
        self.font_id = data[5]
        self.font_scale = data[6]
        self.color = data[7]
        self.alignment = data[8]
        self.unkn_0x24 = data[9]
        self.unkn_0x28 = data[10]
        self.unkn_0x2c = data[11]
        self.unkn_0x30 = data[12]
        self.unkn_0x34 = data[13]
        self.unkn_0x35 = data[14]
        self.html_str = data[15] #.decode('UTF-8', "ignore").strip("\0")

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.unkn_0x0, *self.size, self.font_id, self.font_scale, self.color, self.alignment, self.unkn_0x24, self.unkn_0x28, self.unkn_0x2c, self.unkn_0x30, self.html_str)