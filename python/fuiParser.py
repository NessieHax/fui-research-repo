import struct, os
from dataclasses import dataclass, field
from collections.abc import Callable

import cv2, numpy, zlib

from fuiHeader import fuiHeader
from fuiDataStructures.fuiObject import eFuiObjectType
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
from fuiDataStructures.fuiEdittext import fuiEdittext

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
            "fuiEdittext"           : makeHeaderInfo(self.header.data_counts, 9, 0x138, fuiEdittext), #! 0x70 | unkn int , fuiRect , 1 unkn int, unkn float , fuiRGBA , fuiRect(maybe), 2 unkn int, char html_text_format[0x100 max!], 
            "fuiFontName"           : makeHeaderInfo(self.header.data_counts, 13, 0x104),#! 0x80 | unkn int , char font_name[64], unkn int , char [0x40], unkn int , char [0x40]
            "fuiSymbol"             : makeHeaderInfo(self.header.data_counts, 10, 0x48, fuiSymbol), #! 0x74 | char symbol_name[64] , fuiObject.eFuiObjectType , list index
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
        return -1 < index < self.HeaderDataInfo[section_name].count

    def validate_content_size(self) -> bool:
        size:int = 0
        for _,hInfo in self.HeaderDataInfo.items(): size += hInfo.section_size
        return size == self.header.content_size

    def validate_folder_dest(self, output_path:str) -> str:
        output_path = os.path.join(output_path, f"{self.header.swf_name.replace('.swf','')}")
        try: os.makedirs(output_path)
        #! clear out directory if already exists
        except OSError:
            self.clean(output_path)
        return output_path

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
        for root, dirs, files in os.walk(path):
            if dirs: self.clean(dirs)
            [os.remove(os.path.join(root, file)) for file in files]
    
    def __get_raw_data(self, offset:int, size:int) -> bytearray:
        return self.__raw_data[offset:offset+size]

    def __get_indexed_offset(self, section_name:str, index:int = 0) -> int:
        if not self.is_valid_index(section_name, index): raise Exception("Index out of range")
        return self.get_start_offset_of(section_name) + index * self.__HeaderDataInfo[section_name].element_size

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

    def get_edittext(self) -> list:
        return self.__parsed_objects["fuiEdittext"]

    def __timline_tree(self, timeline:fuiTimeline) -> ...:
        print(timeline)
        for frame in self.get_timeline_frames()[timeline.frame_index:timeline.frame_index + timeline.frame_count]:
            print(f" -> {frame}")
            for evnt in self.get_timeline_events()[frame.event_index:frame.event_index + frame.event_count]:
                print("  -> ",end="")
                print(f"{self.get_timeline_event_names()[evnt.name_index].name}: "if evnt.name_index > -1 else "Unknown: ",end="")
                print(f"{evnt}")
                print("   ",end="")
                if evnt.obj_type == eFuiObjectType.SHAPE and self.is_valid_index("fuiShape", evnt.index):
                    print(f"   -> {self.get_shapes()[evnt.index]}")
                if evnt.obj_type == eFuiObjectType.REFERENCE:
                    print(f"-> {self.get_references()[evnt.index]}")
                if evnt.obj_type == eFuiObjectType.TIMELINE:
                    self.__timline_tree(self.get_timelines()[evnt.index])
                if evnt.obj_type == eFuiObjectType.BITMAP:
                    print(f"-> {self.get_bitmaps()[evnt.index]}")
                if evnt.obj_type == eFuiObjectType.EDITTEXT:
                    print(f"-> {self.get_edittext()[evnt.index]}")
            print()
            for act in self.get_timeline_actions()[timeline.action_index:timeline.action_index + timeline.action_count]:
                print(f" -> {act}")
            print()

    def print_timeline_tree(self) -> None:
        for symbol in self.get_symbols():
            if symbol.obj_type != eFuiObjectType.TIMELINE: continue
            print(symbol.name)
            data = self.get_timelines()[symbol.index]
            self.__timline_tree(data)
            

    def contains_images(self) -> bool:
        return len(self.get_bitmaps()) > 0

    def __decode_image(self, raw_data:bytes | bytearray, read_flags:int = cv2.IMREAD_ANYCOLOR | cv2.IMREAD_UNCHANGED) -> bytearray:
        data = numpy.asarray(bytearray(raw_data), dtype=numpy.uint8)
        return cv2.imdecode(data, read_flags)

    #! JPEG's are stupid lol
    def __insert_zlib_alpha_channel_data(self, bitmap:fuiBitmap, img:numpy.ndarray) -> None:
        if bitmap.zlib_data_offset == 0:
            print("No zlib data offset was provided")
            return
        bufsize = bitmap.size - bitmap.zlib_data_offset
        start_offset = self.get_start_offset_of("images_size")
        data = self.__get_raw_data(start_offset + bitmap.offset + bitmap.zlib_data_offset, bufsize)
        output = zlib.decompress(data, 0, bufsize)
        for i, col in enumerate(img):
            for j, color in enumerate(col):
                alpha_data = output[i*len(col)+j]
                if alpha_data == 0:
                    color[:4] = 0
                    continue
                maxval = 0xff
                color[3] = alpha_data
                x = color[:3] / (alpha_data / maxval)
                x = numpy.nan_to_num(x, nan=maxval, posinf=maxval, neginf=maxval)
                a = numpy.where(maxval-x<=0.0, 255.0, x)
                color[:3] = a.astype(numpy.uint8)

    def __dump_image(self, output_file:str, bitmap:fuiBitmap) -> None:
        data = self.__get_raw_data(self.get_start_offset_of("images_size") + bitmap.offset, bitmap.size)
        ext = "png" if (bitmap.format == 8 or bitmap.format < 6) else "jpeg"
        filename = f"{output_file}.{ext}"
        print("Dumping:", filename[len(os.getcwd()):])
        print(bitmap)
        img = self.__decode_image(data)
        #! TODO: clean up !!
        #!+----------------------------------------+
        final_image = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA if bitmap.format > 5 else cv2.COLOR_BGRA2RGBA) #! no conversion needed for eBitmapFormat.JPEG_NO_ALPHA_DATA
        if bitmap.format == bitmap.eBitmapFormat.JPEG_WITH_ALPHA_DATA and bitmap.zlib_data_offset > 0: self.__insert_zlib_alpha_channel_data(bitmap, final_image)
        write_flags = [cv2.IMWRITE_PNG_COMPRESSION] if ext == "png" else [cv2.IMWRITE_JPEG_QUALITY]
        #!+----------------------------------------+

        cv2.imwrite(filename, final_image, write_flags)


    def dump_images(self, output_path:str) -> None:
        bitmaps = self.get_bitmaps()
        if not self.contains_images():
            print("This fui file does not contain any images")
            return
        output_path = self.validate_folder_dest(output_path)
        count = 0
        for symbol in self.get_symbols():
            if symbol.obj_type != eFuiObjectType.BITMAP: continue
            bitmap = bitmaps[symbol.index]
            self.__dump_image(f"{output_path}/{symbol.name}", bitmap)
            count += 1
        print("Successfully dumped all images!\n" if count == len(bitmaps) else "", end="")

    def dump_raw(self, output_path:str) -> None:
        bitmaps = self.get_bitmaps()
        if not self.contains_images():
            print("This fui file does not contain any images")
            return
        output_path = self.validate_folder_dest(output_path)
        [self.__dump_image(f"{output_path}/image_{i}", bitmap) for i,bitmap in enumerate(bitmaps)]

    def get_start_offset_of(self, section_name:str) -> int:
        if section_name not in self.HeaderDataInfo.keys() or self.HeaderDataInfo[section_name].count == 0: return -1
        offset:int = self.header.header_size
        for key, header_info in self.HeaderDataInfo.items():
            if key == section_name: return offset
            offset += header_info.section_size
        return -1

    def find(self, name:str) -> list[fuiBitmap] | fuiBitmap | list[fuiTimeline] | fuiTimeline | None:
        results = []
        for symbol in self.get_symbols():
            # if symbol.obj_type != eFuiObjectType.BITMAP: continue
            if name.lower() in symbol.name.lower():
                caller, data_type = (self.get_bitmaps, 'fuiBitmap') if symbol.obj_type == eFuiObjectType.BITMAP else (self.get_timelines, 'fuiTimeline')
                data = caller()[symbol.index]
                print(f"{symbol.name} | Offset: {self.__get_indexed_offset(data_type,symbol.index)} | {data}")
                results.append(data)
        if len(results) > 0: return results if len(results) > 1 else results[0]
        print(f"Could not find Symbol named '{name}'")
        return None

    def __str__(self) -> str:
        res:str = ""
        for key, val in self.HeaderDataInfo.items(): res += f"{key} -> {val}\n\n"
        return  res