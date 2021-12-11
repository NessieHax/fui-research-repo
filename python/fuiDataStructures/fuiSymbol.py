from dataclasses import dataclass, field
from typing import overload
import struct

@dataclass(init=False)
class fuiSymbol:
    name:str = field(default_factory=str)
    obj_type:int = field(default_factory=int)
    unk_val:int = field(default_factory=int)
    @overload
    def __init__(self, sym_name:str, Obj_type:int, unkn_val:int): ...
    @overload
    def __init__(self, data:tuple[(str,int,int)]): ...
    @overload
    def __init__(self, raw_bytes:bytes): ...

    def __init__(self, sym_name:str, Obj_type:int, unkn_val:int):
        self.name = sym_name
        self.obj_type = Obj_type
        self.unk_val = unkn_val

    def __init__(self, data:tuple[(str,int,int)]):
        self.name = data[0].decode('UTF-8').strip("\0")
        self.obj_type = data[1]
        self.unk_val = data[2]

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.name = data[0].decode('UTF-8').strip("\0")
        self.obj_type = data[1]
        self.unk_val = data[2]

    @property
    def fmt(self) -> str:
        return "<64s2i"

    def get_name(self) -> str:
        return self.name