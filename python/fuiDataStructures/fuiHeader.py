import struct

from fuiDataStructures.fuiRect import fuiRect

class fuiHeader:
    fmt = "<8sI64s15i4f"
    header_size:int = struct.calcsize(fmt)
    def __init__(self, raw_data:bytes):
        data = struct.unpack(self.fmt, raw_data)
        self.signature:bytes = data[0]
        self.content_size:int = data[1]
        self.import_name:str = data[2].decode("UTF-8").strip("\0")
        self.data_counts:list = [count for count in data[3:18]]
        self.rect:fuiRect = fuiRect(data[18], data[19], data[20], data[21])

    def pack(self) -> bytearray:
        return bytearray(struct.pack(self.fmt, self.signature, self.content_size, self.import_name.encode("UTF-8"), *self.data_counts, *self.rect))

    def __repr__(self):
        return f"""
Version: {self.signature[0]}
Signature: {self.signature}
Content Size: {self.content_size}
Header Size: {self.header_size}
Import Name: {self.import_name}
Stage Size: {self.rect.get_size()}
{self.data_counts}
"""