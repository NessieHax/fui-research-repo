from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiObject import fuiObject

@dataclass(init=False)
class fuiTimelineAction(fuiObject):
    fmt = "<2bh64s64s"
    size = struct.calcsize(fmt)

    #! fuiRenderNodeTimeline::handleConstruction
    #! TODO
    action_type:int
    unkn_0x1:int
    frame_index:int #! -1 if not needed/used
    action_arg0:str
    action_arg1:str

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.action_type = data[0]
        self.unkn_0x1 = data[1]
        self.frame_index = data[2]
        self.action_arg0 = data[3].decode('UTF-8').strip("\0")
        self.action_arg1 = data[4].decode('UTF-8').strip("\0")

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.action_type, self.unkn_0x1, self.frame_index, self.action_arg0.encode("UTF-8"), self.action_arg1.encode("UTF-8"))