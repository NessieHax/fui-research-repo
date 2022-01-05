from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiRect import fuiRect

@dataclass(init=False)
class fuiTimeline:
    fmt = f"<i4h{fuiRect.fmt}"

    symbol_index:int = field(default_factory=int)
    frame_index:int = field(default_factory=int)
    frame_count:int = field(default_factory=int)
    action_index:int = field(default_factory=int)
    action_count:int = field(default_factory=int)
    rect:fuiRect = field(default_factory=fuiRect)
    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.symbol_index = data[0]
        self.frame_index = data[1]
        self.frame_count = data[2]
        self.action_index = data[3]
        self.action_count = data[4]
        self.rect = fuiRect(data[5], data[6], data[7], data[8])

    def pack(self) -> bytearray:
        return bytearray(struct.pack(self.fmt, self.symbol_index, self.frame_index, self.frame_count, self.action_index, self.action_count, *self.rect))