import struct, os
from dataclasses import dataclass, field
from collections.abc import Callable

import cv2, numpy 

from fuiHeader import fuiHeader
from fuiDataStructures.fuiImportAsset import fuiImportAsset
from fuiDataStructures.fuiBitmap import fuiBitmap
from fuiDataStructures.fuiSymbol import fuiSymbol
from fuiDataStructures.fuiTimeline import fuiTimeline
from fuiDataStructures.fuiReference import fuiReference
from fuiDataStructures.fuiVert import fuiVert
from fuiDataStructures.fuiTimelineEvent import fuiTimelineEvent
from fuiDataStructures.fuiTimelineFrame import fuiTimelineFrame
from fuiDataStructures.fuiTimelineEventName import fuiTimelineEventName
from fuiDataStructures.fuiTimelineAction import fuiTimelineAction
from fuiDataStructures.fuiShape import fuiShape
from fuiDataStructures.fuiShapeComponent import fuiShapeComponent

@dataclass
class HeaderInfo:
    count:int = field(default_factory=int)
    element_size:int = field(default_factory=int)
    section_size:int = field(default_factory=int)
    repr_cls:Callable[[],None] = field(repr=False,default_factory=Callable[[],None])

def makeHeaderInfo(data:list , index:int, element_size:int, cls = None) -> HeaderInfo:
    return HeaderInfo(data[index], element_size, data[index]*element_size, cls)

class fuiParser:
    def __init__(self, raw_fui_file:bytes):
        self.header:fuiHeader = fuiHeader(raw_fui_file[:0x98])
        self.__raw_data:bytearray = raw_fui_file
        self.__HeaderDataInfo:dict = {
            "fuiTimeline"           : makeHeaderInfo(self.header.data_counts, 0, 0x1c, fuiTimeline),  #! 0x4c | fuiObject.eFuiObjectType , 4 unkn short , fuiRect
            "fuiTimelineAction"     : makeHeaderInfo(self.header.data_counts, 2, 0x84, fuiTimelineAction),  #! 0x54 | unkn short , unnk short(swapped) , char unkn_buf[64](action??) , char unkn_buf[64](argv??) 
            "fuiShape"              : makeHeaderInfo(self.header.data_counts, 3, 0x1c, fuiShape),  #! 0x58 | 2 Intiger(need swap), fuiObject.eFuiObjectType , fuiRect
            "fuiShapeComponent"     : makeHeaderInfo(self.header.data_counts, 4, 0x2c, fuiShapeComponent),  #! 0x5c | fuiFillStyle , 2 Intiger(need swap)
            "fuiVert"               : makeHeaderInfo(self.header.data_counts, 5, 0x8, fuiVert),   #! 0x60 | fuiVert(float x, float y)
            "fuiTimelineFrame"      : makeHeaderInfo(self.header.data_counts, 6, 0x48, fuiTimelineFrame),  #! 0x64 | char frame_name[64] , 2 Intiger(need swap)
            "fuiTimelineEvent"      : makeHeaderInfo(self.header.data_counts, 7, 0x48, fuiTimelineEvent),  #! 0x68 | 4 unkn short , fuiMatrix , fuiColorTransform , fuiRGBA
            "fuiTimelineEventName"  : makeHeaderInfo(self.header.data_counts, 1, 0x40, fuiTimelineEventName),  #! 0x50 | char Name[64]
            "fuiReference"          : makeHeaderInfo(self.header.data_counts, 8, 0x48, fuiReference),  #! 0x6c | fuiObject.eFuiObjectType , char ref_name[64] , unknown value(needs swap)
            "fuiEdittext"           : makeHeaderInfo(self.header.data_counts, 9, 0x138), #! 0x70 | unkn int , fuiRect , 1 unkn int, unkn float , fuiRGBA , fuiRect(maybe), 2 unkn int, char html_text_format[0x100 max!], 
            "fuiFontName"           : makeHeaderInfo(self.header.data_counts, 13, 0x104),#! 0x80 | unkn int , char font_name[64], unkn int , char [0x40], unkn int , char [0x40]
            "fuiSymbol"             : makeHeaderInfo(self.header.data_counts, 10, 0x48, fuiSymbol), #! 0x74 | char symbol_name[64] , fuiObject.eFuiObjectType , unkn int
            "fuiImportAsset"        : makeHeaderInfo(self.header.data_counts, 14, 0x40, fuiImportAsset), #! 0x84 | char asset_name[64]
            "fuiBitmap"             : makeHeaderInfo(self.header.data_counts, 11, 0x20, fuiBitmap), #! 0x78 | fuiObject.eFuiObjectType , unkn int , width(int swapped) , height(int swapped) , unkn int , compressed_image_size(png/jpeg compression)
            "images_size"           : makeHeaderInfo(self.header.data_counts, 12, 0x1),  #! 0x7c | size of bytes at the end
        }
        #! dictionary containing dataclasses to represent objects in a fui file
        self.__parsed_objects:dict = {
            "fuiTimeline" : [],
            "fuiTimelineAction" : [],
            "fuiShape" : [],
            "fuiShapeComponent" : [],
            "fuiVert" : [],
            "fuiTimelineFrame" : [],
            "fuiTimelineEvent" : [],
            "fuiTimelineEventName" : [],
            "fuiReference" : [],
            "fuiEdittext" : [],
            "fuiFontName" : [],
            "fuiSymbol" : [],
            "fuiImportAsset" : [],
            "fuiBitmap" : [],
            "images_size" : 0
        }

    @property
    def HeaderDataInfo(self) -> dict:
        return self.__HeaderDataInfo

    def validate_class_size(self, section_name:str, cls) -> bool:
        """ Returns `true` if the fmt property of a class equals the data type element size """
        return self.HeaderDataInfo[section_name].element_size == struct.calcsize(cls.fmt)

    def is_valid_index(self, section_name:str, index:int) -> bool:
        return index < self.HeaderDataInfo[section_name].count and index > -1

    def validate_content_size(self) -> bool:
        size:int = 0
        for _,hInfo in self.HeaderDataInfo.items(): size += hInfo.section_size
        return size == self.header.content_size

    def validate_folder_dest(self, output_path:str) -> None:
        try: os.makedirs(output_path)
        #! clear out directory if already exists
        except OSError: 
            self.clean(output_path)

    #! sets up Object lists
    def parse(self) -> None:
        [self.__parse(key, self.__parsed_objects[key]) for key,data in self.HeaderDataInfo.items() if data.repr_cls is not None]
        self.__parsed_objects["images_size"] = self.HeaderDataInfo["images_size"].section_size

    def __parse(self, section_name:str, container:list) -> list:
        cls = self.HeaderDataInfo[section_name].repr_cls
        if not self.validate_class_size(section_name, cls): raise Exception("Class does not contain the required size!")
        for i in range(self.HeaderDataInfo[section_name].count):
            offset = self.__get_indexed_offset(section_name, i)
            data_size = self.HeaderDataInfo[section_name].element_size
            container.append(cls(self.__get_raw_data(offset, data_size)))
        return container

    def rebuild(self) -> None:
        pass

    #! TODO: make this robust | folder deletion
    def clean(self, path:str) -> None:
        for root, _, files in os.walk(path):
            [os.remove(os.path.join(root, file)) for file in files]
    
    def __get_raw_data(self, offset:int, size:int) -> bytearray:
        return self.__raw_data[offset:offset+size]

    def __get_indexed_offset(self, section_name:str, index:int = 0) -> int:
        if not self.is_valid_index(section_name, index): raise Exception("Index out of range")
        return self.get_start_offset_of(section_name) + index * self.__HeaderDataInfo[section_name].element_size if index < self.__HeaderDataInfo[section_name].count else -1

    def get_imported_assets(self) -> list:
        return self.__parsed_objects["fuiImportAsset"]

    def get_fonts(self) -> list:
        return self.__parsed_objects["fuiFontName"]

    def get_symbols(self) -> list:
        return self.__parsed_objects["fuiSymbol"]

    def get_timeline_frames(self) -> list:
        return self.__parsed_objects["fuiTimelineFrame"]

    def get_timeline_actions(self) -> list:
        return self.__parsed_objects["fuiTimelineAction"]

    def get_references(self) -> list:
        return self.__parsed_objects["fuiReference"]

    def get_bitmaps(self) -> list:
        return self.__parsed_objects["fuiBitmap"]

    def get_timeline_events(self) -> list:
        return self.__parsed_objects["fuiTimelineEvent"]

    def get_timeline_event_names(self) -> list:
        return self.__parsed_objects["fuiTimelineEventName"]
    
    def get_timelines(self) -> list:
        return self.__parsed_objects["fuiTimeline"]

    def get_vert(self) -> list:
        return self.__parsed_objects["fuiVert"]

    def get_shapes(self) -> list:
        return self.__parsed_objects["fuiShape"]

    def get_shape_components(self) -> list:
        return self.__parsed_objects["fuiShapeComponent"]

    def __dump_image(self, output_file:str, start_offset:int, size:int) -> None:
        png_header_magic = b'PNG'
        out_data = self.__get_raw_data(start_offset, size)
        ext:str = "png" if out_data[1:4] == png_header_magic else "jpeg"
        filename = f"{output_file}.{ext}"
        # print("Dumping:",filename)
        if ext == "png": 
            data = numpy.asarray(bytearray(out_data), dtype=numpy.uint8)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR | cv2.IMREAD_UNCHANGED)
            image_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
            cv2.imwrite(filename, image_rgb, [cv2.IMWRITE_PNG_COMPRESSION])
            return
        with open(filename, "wb") as out: out.write(out_data)

    #! Dumps to output_path/fui_file_name/
    def dump_images(self, output_path:str) -> None:
        header_info = self.HeaderDataInfo["fuiBitmap"]
        start:int = self.get_start_offset_of("fuiBitmap")
        image_data_start:int = start + header_info.section_size
        bitmaps = self.get_bitmaps()
        if len(bitmaps) == 0:
            print("This fui file does not contain any images")
            return

        output_path = f"{output_path}/{self.header.swf_name.replace('.swf','')}"
        self.validate_folder_dest(output_path)

        # image_count = 0
        for symbol in self.get_symbols():
            if symbol.obj_type == 3: 
                # image_count += 1
                bitmap_data = bitmaps[symbol.index]
                # print(f"{symbol.name}({symbol.index}):\n\t{bitmap_data}")
                image_start:int = image_data_start + bitmap_data.offset
                self.__dump_image(f"{output_path}/{symbol.name}", image_start, bitmap_data.size)

        # print("Dumped:",image_count)
        # print("Contained:",len(self.get_bitmaps()))

    def dump_raw(self, output_path:str) -> None:
        output_path = f"{output_path}/{self.header.swf_name.replace('.swf','')}"
        self.validate_folder_dest(output_path)
        header_info = self.HeaderDataInfo["fuiBitmap"]
        start:int = self.get_start_offset_of("fuiBitmap")
        image_data_start:int = start + header_info.section_size
        for i,bitmap in enumerate(self.get_bitmaps()):
            image_start:int = image_data_start + bitmap.offset
            self.__dump_image(f"{output_path}/image_{i}", image_start, bitmap.size)

    def get_start_offset_of(self, section_name:str) -> int:
        if section_name not in self.HeaderDataInfo.keys() or self.HeaderDataInfo[section_name].count == 0: return -1
        offset:int = self.header.header_size
        for key, header_info in self.HeaderDataInfo.items():
            if key == section_name: return offset
            offset += header_info.section_size
        return -1

    def get_image_by_name(self, name:str) -> fuiBitmap:
        for symbol in self.get_symbols():
            if symbol.obj_type != 3: continue
            if symbol.name == name:
                print(self.__get_indexed_offset("fuiBitmap",symbol.index))
                return self.get_bitmaps()[symbol.index]
        raise Exception(f"Could not find image named '{name}'")

    def __str__(self) -> str:
        res:str = ""
        for key, val in self.HeaderDataInfo.items(): res += f"{key} -> {val}\n\n"
        return  res