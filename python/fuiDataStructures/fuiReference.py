from dataclasses import dataclass, field
# from typing import overload
import struct

@dataclass(init=False)
class fuiReference:
    fmt = "<i64si"

    symbol_index:int = field(default_factory=int)
    reference:str = field(default_factory=str)
    fui_file_index:int = field(default_factory=int)#

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.symbol_index = data[0]
        self.reference = data[1].decode('UTF-8').strip("\0")
        self.fui_file_index = data[2]