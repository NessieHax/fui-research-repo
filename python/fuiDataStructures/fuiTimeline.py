from dataclasses import dataclass, field
# from typing import overload
import struct

from fuiDataStructures.fuiRect import fuiRect

@dataclass(init=False)
class fuiTimeline:
    unkn_0x0:int = field(default_factory=int)
    unkn_0x4:int = field(default_factory=int)
    unkn_0x6:int = field(default_factory=int)
    unkn_0x8:int = field(default_factory=int)
    unkn_0xa:int = field(default_factory=int)
    rect:fuiRect = field(repr=False) #! TODO: get fuiRect.__str__ working with dataclass __repr__
    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.unkn_0x0 = data[0]
        self.unkn_0x4 = data[1]
        self.unkn_0x6 = data[2]
        self.unkn_0x8 = data[3]
        self.unkn_0xa = data[4]
        self.rect = fuiRect(data[5], data[6], data[7], data[8])
    
    @property
    def fmt(self) -> str:
        return "<i4h4f"