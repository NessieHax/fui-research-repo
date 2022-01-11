from dataclasses import dataclass, field
import struct

from fuiDataStructures.fuiObject import fuiObject
@dataclass(init=False)
class fuiBitmap(fuiObject):
    fmt = "<8i"

    class eBitmapFormat:
        PNG_WITH_ALPHA_DATA:int = 1 #! fully ignored
        PNG_NO_ALPHA_DATA:int = 3   #! fully ignored
        JPEG_NO_ALPHA_DATA:int = 6
        JPEG_UNKNOWN:int = 7 #! TODO: find name
        JPEG_WITH_ALPHA_DATA:int = 8

    symbol_index:int = field(default_factory=int)
    format:int = field(default_factory=int)
    width:int = field(default_factory=int)
    height:int = field(default_factory=int)
    offset:int = field(default_factory=int)
    size:int = field(default_factory=int)
    zlib_data_start:int = field(default_factory=int)
    unkn_0x1c:int = field(default_factory=int)

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.symbol_index = data[0]
        self.format = data[1]
        self.width = data[2]
        self.height = data[3]
        self.offset = data[4]
        self.size = data[5]
        self.zlib_data_start = data[6]
        self.unkn_0x1c = data[7] #! set to -1 if they was an error at runtime

    def pack(self) -> bytearray:
        return bytearray(struct.pack(self.fmt, self.symbol_index, self.format, self.width, self.height, self.offset, self.size, self.zlib_data_start, self.unkn_0x1c))