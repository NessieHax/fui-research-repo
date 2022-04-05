from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiObject import fuiObject

@dataclass(init=False)
class fuiReference(fuiObject):
    fmt = "<i64si"

    symbol_index:int
    reference:str
    fui_file_index:int

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.symbol_index = data[0]
        self.reference = data[1].decode('UTF-8').strip("\0")
        self.fui_file_index = data[2]

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.symbol_index, self.reference.encode('UTF-8'), self.fui_file_index)