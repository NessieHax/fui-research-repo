import struct
from dataclasses import dataclass, field

from fuiHeader import fuiHeader, swapLE32

@dataclass
class HeaderInfo:
    count:int = field()
    element_size:int = field()
    section_size:int = field()

def makeHeaderInfo(data:list , index:int, element_size:int) -> HeaderInfo:
    return HeaderInfo(data[index], element_size, data[index]*element_size)

class fuiParser:
    def __init__(self, raw_fui_file:bytes):
        self.__header:fuiHeader = fuiHeader(raw_fui_file[0:0x98])
        self.__raw_data:bytearray = raw_fui_file
        self.__HeaderDataInfo:dict = {
            "fuiTimeline"           : makeHeaderInfo(self.__header.data_counts, 0, 0x1c),  #! 0x4c | fuiObject.eFuiObjectType , 4 unkn short , fuiRect
            "fuiTimelineAction"     : makeHeaderInfo(self.__header.data_counts, 2, 0x84),  #! 0x54 | unkn short , unnk short(swapped) , char unkn_buf[64](action??) , char unkn_buf[64](argv??) 
            "fuiShape"              : makeHeaderInfo(self.__header.data_counts, 3, 0x1c),  #! 0x58 | 2 Intiger(need swap), fuiObject.eFuiObjectType , fuiRect
            "fuiShapeComponent"     : makeHeaderInfo(self.__header.data_counts, 4, 0x2c),  #! 0x5c | fuiFillStyle , 2 Intiger(need swap)
            "fuiVert"               : makeHeaderInfo(self.__header.data_counts, 5, 0x8),   #! 0x60 | fuiVert(float x, float y)
            "fuiTimelineFrame"      : makeHeaderInfo(self.__header.data_counts, 6, 0x48),  #! 0x64 | char frame_name[64] , 2 Intiger(need swap)
            "fuiTimelineEvent"      : makeHeaderInfo(self.__header.data_counts, 7, 0x48),  #! 0x68 | 4 unkn short , fuiMatrix , fuiColorTransform , fuiRGBA
            "fuiTimelineEventName"  : makeHeaderInfo(self.__header.data_counts, 1, 0x40),  #! 0x50 | char Name[64]
            "fuiReference"          : makeHeaderInfo(self.__header.data_counts, 8, 0x48),  #! 0x6c | fuiObject.eFuiObjectType , char ref_name[64] , unknown value(needs swap)
            "fuiEdittext"           : makeHeaderInfo(self.__header.data_counts, 9, 0x138), #! 0x70 | unkn int , fuiRect , 1 unkn int, unkn float , fuiRGBA , fuiRect(maybe), 2 unkn int, char html_text_format[0x100 max!], 
            "fuiFontName"           : makeHeaderInfo(self.__header.data_counts, 13, 0x104),#! 0x80 | unkn int , char font_name[64], unkn int , char [0x40], unkn int , char [0x40]
            "fuiSymbol"             : makeHeaderInfo(self.__header.data_counts, 10, 0x48), #! 0x74 | char symbol_name[64] , fuiObject.eFuiObjectType , unkn int
            "fuiImportAsset"        : makeHeaderInfo(self.__header.data_counts, 14, 0x40), #! 0x84 | char asset_name[64]
            "fuiBitmap"             : makeHeaderInfo(self.__header.data_counts, 11, 0x20), #! 0x78 | fuiObject.eFuiObjectType , unkn int , width(int swapped) , height(int swapped) , unkn int , compressed_image_size(png/jpeg compression)
            "images_size"           : makeHeaderInfo(self.__header.data_counts, 12, 0x1),  #! 0x7c | size of bytes at the end
        }

    def parse(self) -> None:
        pass

    @property
    def HeaderDataInfo(self) -> dict:
        return self.__HeaderDataInfo

    @property
    def header(self) -> fuiHeader:
        return self.__header

    def __get_data_format(self, data_format:str, offset:int) -> tuple:
        size:int = struct.calcsize(data_format)
        return struct.unpack(data_format, self.__raw_data[offset:offset+size])

    def __get_data(self, offset:int, size:int) -> bytearray:
        return self.__get_data_format(f"{size}s", offset)[0]

    def __get_data_by_section_name(self, section_name:str, index:int = 0) -> bytearray:
        offset:int = self.get_start_offset_of(section_name) + index * self.__HeaderDataInfo[section_name].element_size
        return self.__get_data(offset, self.__HeaderDataInfo[section_name].element_size)
    
    def __get_string(self, section_name:str, index:int, string_buffer_size:int, padding_before:int = 0, padding_after:int = 0) -> str:
        return self.__get_data_by_section_name(section_name, index)[padding_before:string_buffer_size].decode("UTF-8").replace("\0","")

    def __get_strings(self, section_name:str, string_buffer_size:int, padding_before:int = 0, padding_after:int = 0) -> list:
        return [self.__get_string(section_name, i, string_buffer_size, padding_before=padding_before, padding_after=padding_after) for i in range(self.HeaderDataInfo[section_name].count)]

    def get_imported_assets(self) -> list:
        return self.__get_strings("fuiImportAsset", 0x40)

    def get_fonts(self) -> list:
        return self.__get_strings("fuiFontName", 0x40, padding_before=4, padding_after=0xc0)

    def get_symbols(self) -> list:
        return self.__get_strings("fuiSymbol", 0x40, padding_after=8)

    def get_timeline_events(self) -> list:
        return self.__get_strings("fuiTimelineEventName", 0x40)

    def get_timeline_frames(self) -> list:
        return self.__get_strings("fuiTimelineFrame", 0x40, padding_after=8)

    def get_timeline_actions(self) -> list:
        return self.__get_strings("fuiTimelineAction", 0x80, padding_before=4)

    def get_references(self) -> list:
        return self.__get_strings("fuiReference", 0x40, padding_before=4, padding_after=4)

    def get_bitmaps(self) -> list:
        return [self.__get_data_format("<8x4I8x", self.get_start_offset_of("fuiBitmap") + i * self.__HeaderDataInfo["fuiBitmap"].element_size) for i in range(self.__HeaderDataInfo["fuiBitmap"].count)]

    def get_images(self, output_path:str) -> None:
        header_info = self.HeaderDataInfo["fuiBitmap"]
        count, element_size, size  = header_info.count, header_info.element_size, header_info.section_size
        start:int = self.get_start_offset_of("fuiBitmap")
        image_start:int = start + size
        png_header_magic = b'\x89PNG'

        # symbols = self.get_symbols()
        bitmaps = self.get_bitmaps()
        # print(f"{bitmaps=}")
        for i, (w,h, size1, size2) in enumerate(bitmaps):
            # is_bitmap = sym_data["end_padd"][0] == 3
            # if not is_bitmap: continue
            # print(f"\n{sym_text}: {is_bitmap=}")
            print(self.__get_string("fuiSymbol", i, 0x40))

            fmt:str = "<8x2I4xI8x"
            pos:int = start + i * element_size
            buffer:bytes = self.__get_data(pos, element_size)
            buffer = struct.unpack(fmt, buffer)
            # print(f"{buffer[0]}x{buffer[1]}") #! scale Width and hight used in game
            image_size = buffer[2]
            out_data = self.__get_data(image_start, image_size)
            ext:str = "png" if out_data[0:4] == png_header_magic else "jpeg"
            image_start += image_size
            with open(f"{output_path}/image_{i}.{ext}", "wb") as out: out.write(out_data)
        print(f"Dumped {count} images")

    def get_start_offset_of(self, section_name:str) -> int:
        if section_name not in self.HeaderDataInfo.keys() or self.HeaderDataInfo[section_name].count == 0: return -1
        offset:int = self.__header.HeaderSize
        for key, header_info in self.HeaderDataInfo.items():
            if key == section_name: return offset
            offset += header_info.section_size
        return -1

    def get_sections_size(self) -> int:
        size:int = 0
        for _,[_,_,s] in self.HeaderDataInfo.items(): size += s
        return size

    def __str__(self) -> str:
        res:str = self.__header.__str__() + "\n"
        for key, val in self.HeaderDataInfo.items(): res += f"{key} -> {val}\n\n"
        return  res