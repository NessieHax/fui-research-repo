from typing import Optional

from fuiParser import fuiParser
from fuiDataStructures.fuiHeader import fuiHeader

class fuiBuilder:
    def __init__(self) -> None: ...

    def create_blank_fuiheader(self) -> fuiHeader:
        header = fuiHeader(bytearray(fuiHeader.header_size))
        header.signature = b'\x01IUF\0\0\0\0' # Default signature
        header.import_name = "MIKU_BLANK_FUI"
        #! rect size may vary depending on the console
        header.rect.set_x(0.0, 1280.0)
        header.rect.set_y(0.0, 720.0)
        return header

    #! TODO
    def build_from_parser(self, parser:fuiParser, file_name:Optional[str] = None) -> None:
        header = parser.get_header()

        file = file_name if file_name is not None else f"mod_{header.import_name.replace('.swf','')}"
        file += ".fui"

        with open(file, "wb") as modified:
            modified.write(header.pack())
            output:bytearray = bytearray()

            for key, data_list in parser._parsed_objects.items():
                for data in data_list:
                    if key == "images":
                        output += data
                        continue
                    output += data.pack()
            
            modified.write(output)


    #! TODO
    def __setup_header(self) -> None: ...

    #! TODO
    def __calc_content_size_and_set_header_counts(self) -> int: ...