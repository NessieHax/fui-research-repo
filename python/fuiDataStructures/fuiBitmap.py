from dataclasses import dataclass
import struct

from fuiDataStructures.fuiObject import fuiObject
@dataclass(init=False)
class fuiBitmap(fuiObject):
    fmt = "<8i"
    size = struct.calcsize(fmt)

    class eFuiBitmapType:
        PNG_WITH_ALPHA_DATA:int = 1 #! fully ignored
        PNG_NO_ALPHA_DATA:int = 3   #! fully ignored
        JPEG_NO_ALPHA_DATA:int = 6
        JPEG_UNKNOWN:int = 7 #! TODO: find name
        JPEG_WITH_ALPHA_DATA:int = 8 #! if set the zlib_data_start has to be set

    symbol_index:int
    format:int
    width:int
    height:int
    offset:int
    size:int
    zlib_data_start:int
    texture_bind_handle:int

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.symbol_index = data[0]
        self.format = data[1]
        self.width = data[2]
        self.height = data[3]
        self.offset = data[4]
        self.size = data[5]
        self.zlib_data_start = data[6]
        self.texture_bind_handle = data[7]

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.symbol_index, self.format, self.width, self.height, self.offset, self.size, self.zlib_data_start, self.texture_bind_handle)