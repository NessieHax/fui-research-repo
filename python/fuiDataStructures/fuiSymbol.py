from dataclasses import dataclass, field
from typing import overload
import struct

@dataclass(init=False)
class fuiSymbol:
    fmt = "<64s2i"

    name:str = field(default_factory=str)
    obj_type:int = field(default_factory=int)
    index:int = field(default_factory=int) #! TODO: find a proper name | DESC.: used to map symbol to specific type list
    @overload
    def __init__(self, sym_name:str, Obj_type:int, unkn_val:int): ...
    @overload
    def __init__(self, data:tuple[(str,int,int)]): ...
    @overload
    def __init__(self, raw_bytes:bytes): ...

    def __init__(self, sym_name:str, Obj_type:int, unkn_val:int):
        self.name = sym_name
        self.obj_type = Obj_type
        self.index = unkn_val

    def __init__(self, data:tuple[(str,int,int)]):
        self.name = data[0].decode('UTF-8').strip("\0")
        self.obj_type = data[1]
        self.index = data[2]

    def __init__(self, raw_bytes:bytes):
        data = struct.unpack(self.fmt, raw_bytes)
        self.name = data[0].decode('UTF-8').strip("\0")
        self.obj_type = data[1]
        self.index = data[2]


    def get_name(self) -> str:
        return self.name