from dataclasses import dataclass, field
import struct

@dataclass(init=False)
class fuiSymbol:
    fmt = "<64s2i"

    name:str = field(default_factory=str)
    obj_type:int = field(default_factory=int)
    index:int = field(default_factory=int) #! TODO: find a proper name | DESC.: used to map symbol to specific type list

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.name = data[0].decode('UTF-8').strip("\0")
        self.obj_type = data[1]
        self.index = data[2]

    def pack(self) -> bytearray:
        return bytearray(struct.pack(self.fmt, self.name.encode('UTF-8'), self.obj_type, self.index))