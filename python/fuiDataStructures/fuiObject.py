
class eFuiObjectType:
    STAGE = 0
    SHAPE = 1
    TIMELINE = 2
    BITMAP = 3
    REFERENCE = 4
    EDITTEXT = 5
    CODEGENRECT = 6

class fuiObject:
    def __init__(self, _type:int):
        self.type:int = _type