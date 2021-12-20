import struct

from fuiDataStructures.fuiRect import fuiRect

class fuiHeader:
    fmt = "<4s4xI64s15i4f"
    header_size:int = struct.calcsize(fmt)
    def __init__(self, raw_data:bytes):
        data = struct.unpack(self.fmt, raw_data)
        self.version = data[0][0]
        self.identifier:str = data[0][1:4] #! loaded : "FUI" | stored : "IUF"
        self.content_size:int = data[1] #! header_size + content_size = whole file size
        self.swf_name:str = data[2].decode("UTF-8").strip("\0")
        self.data_counts:list = [count for count in data[3:18]]
        self.rect:fuiRect = fuiRect(data[18], data[19], data[20], data[21])

    def __repr__(self):
        return f"""
Version: {self.version}
Identifier: {self.identifier}
Content Size: {self.content_size}
Header Size: {self.header_size}
Swf Name: {self.swf_name}
Stage: {self.rect}
Stage Size: {self.rect.get_size()}
"""
# Object Counts: {self.data_counts}