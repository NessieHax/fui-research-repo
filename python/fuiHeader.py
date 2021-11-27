import struct
from enum import Enum

from fuiRect import fuiRect

def swapLE32(x , fmt:str):
    return struct.unpack(fmt.replace(">", "<"), struct.pack(fmt,x))[0]

class eFuiObjectType(Enum):
    Stage = 0
    Shape = 1
    Timeline = 2
    Bitmap = 3
    EditText = 5
    CodeGenRect = 6

class fuiHeader:
    def __init__(self, rawHeader:bytes):
        fmt = "<4s4xI64s15I4f"
        data = struct.unpack(fmt, rawHeader)
        self.identifier:str = data[0] #! loaded : "FUI\x01" file : "\x01IUF"
        self.size:int = data[1] #! HeaderSize + size = whole file size
        self.swfname:str = data[2].decode("UTF-8").replace("\x00","")
        self.data_counts:list = [cluster_counter for cluster_counter in data[3:18]] #! count of data cluster(fuiTimeline/fuiBitmap/etc..)
        self.rect:fuiRect = fuiRect(data[18], data[20], data[19], data[21])
        self.HeaderSize:int = struct.calcsize(fmt)

    def __repr__(self):
        return f"""
Identifier: {self.identifier}
Content Size: {self.size}
Header Size: {self.HeaderSize}
Swf Name: {self.swfname}
Frame: {self.rect}

Cluster Counts: {self.data_counts}
"""