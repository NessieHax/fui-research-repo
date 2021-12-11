from enum import Enum

class eFuiObjectType(Enum):
    Stage = 0
    Shape = 1
    Timeline = 2
    Bitmap = 3
    EditText = 5
    CodeGenRect = 6

class fuiObject:
    def __init__(self, _type:eFuiObjectType):
        self.type:eFuiObjectType = _type