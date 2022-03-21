import abc

class eFuiObjectType:
    STAGE = 0
    SHAPE = 1
    TIMELINE = 2
    BITMAP = 3
    REFERENCE = 4
    EDITTEXT = 5
    CODEGENRECT = 6

class fuiObject(metaclass=abc.ABCMeta):
    fmt:str
    @abc.abstractmethod
    def __init__(self, bytes:bytes) -> None: ...
    @abc.abstractmethod
    def pack(self) -> bytearray: ...