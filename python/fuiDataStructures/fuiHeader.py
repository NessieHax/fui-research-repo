import struct

from fuiDataStructures.fuiRect import fuiRect
from fuiDataStructures.fuiObject import fuiObject

class fuiHeader(fuiObject):
    fmt = "<8sI64s15i4f"
    size = struct.calcsize(fmt)
    def __init__(self, raw_data:bytes):
        data = struct.unpack(self.fmt, raw_data)
        self.signature:bytes = data[0]
        self.content_size:int = data[1]
        self.import_name:str = data[2].decode("UTF-8").strip("\0")
        self.data_counts = (self.timeline_count, self.timeline_event_name_count, self.timeline_action_count,
         self.shape_count, self.shape_component_count, self.vert_count,
         self.timeline_frame_count, self.timeline_event_count, self.reference_count,
         self.edittext_count, self.symbol_count, self.bitmap_count,
         self.image_sizes, self.font_name_count, self.import_asset_count
        ) = data[3:18]
        self.rect:fuiRect = fuiRect(data[18], data[19], data[20], data[21])

    def pack(self) -> bytes:
        return struct.pack(self.fmt, self.signature, self.content_size, self.import_name.encode("UTF-8"), *self.data_counts, *self.rect)

    def __repr__(self):
        return f"""
Version: {self.signature[0]}
Signature: {self.signature[1:]}
Content Size: {self.content_size}
Header Size: {self.size}
Import Name: {self.import_name}
Stage Size: {self.rect.get_size()}
{self.data_counts}
"""