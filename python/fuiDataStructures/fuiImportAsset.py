from dataclasses import dataclass, field
# from typing import overload
import struct

@dataclass(init=False)
class fuiImportAsset:
    import_name:str = field(default_factory=str)

    def __init__(self, raw_bytes:bytes):
        self.import_name = struct.unpack(self.fmt, raw_bytes)[0].decode('UTF-8').strip("\0")
        
    @property
    def fmt(self) -> str:
        return "<64s"