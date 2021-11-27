import struct

from fuiObject import fuiObject
from fuiRect import fuiRect

class fuiTimeline:
    def __init__(self, raw_bytes:bytes):
        fmt:str = "<I4h4f"
        data = struct.unpack(fmt, raw_bytes)
        self.members:dic = {
            "fuiObject" : data[0],
            "_0x4" : data[1],
            "_0x6" : data[2],
            "_0x8" : data[3],
            "_0xa" : data[4],
            "rect" : fuiRect(data[5], data[7], data[6], data[8])
        }

    def __str__(self):
        res:str = ""
        for key, val in self.members.items(): res += f"{key} -> Data: {val}\n\n"
        return res