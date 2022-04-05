import struct
from dataclasses import dataclass, field

from fuiDataStructures.fuiObject import fuiObject
@dataclass(init=False)
class fuiSymbol(fuiObject):
    fmt = "<64s2i"

    name:str
    obj_type:int
    #! TODO: find a proper name | DESC.: used to map symbol to specific type list
    index:int

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.name = data[0].decode('UTF-8').strip("\0")
        self.obj_type = data[1]
        self.index = data[2]

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.name.encode('UTF-8'), self.obj_type, self.index)