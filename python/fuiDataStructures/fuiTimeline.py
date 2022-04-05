from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiRect import fuiRect
from fuiDataStructures.fuiObject import fuiObject

@dataclass(init=False)
class fuiTimeline(fuiObject):
    fmt = f"<i4h{fuiRect.fmt}"

    symbol_index:int
    frame_index:int
    frame_count:int
    action_index:int
    action_count:int
    rect:fuiRect = field(default_factory=fuiRect)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.symbol_index = data[0]
        self.frame_index = data[1]
        self.frame_count = data[2]
        self.action_index = data[3]
        self.action_count = data[4]
        self.rect = fuiRect(data[5], data[6], data[7], data[8])

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.symbol_index, self.frame_index, self.frame_count, self.action_index, self.action_count, *self.rect)