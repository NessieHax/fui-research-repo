import struct, os, cv2, numpy, zlib
from dataclasses import dataclass, field
from collections.abc import Callable

from fuiDataStructures.fuiHeader import fuiHeader
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
from fuiDataStructures.fuiFontName import fuiFontName

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
        self.__header:fuiHeader = fuiHeader(raw_fui_file[:fuiHeader.header_size])
        self.__raw_data:bytes = raw_fui_file
        self.__HeaderDataInfo:dict = {
            "fuiTimeline"           : makeHeaderInfo(self.__header.data_counts, 0, 0x1c, fuiTimeline), #! 0x4c
            "fuiTimelineAction"     : makeHeaderInfo(self.__header.data_counts, 2, 0x84, fuiTimelineAction), #! 0x54
            "fuiShape"              : makeHeaderInfo(self.__header.data_counts, 3, 0x1c, fuiShape), #! 0x58
            "fuiShapeComponent"     : makeHeaderInfo(self.__header.data_counts, 4, 0x2c, fuiShapeComponent), #! 0x5c
            "fuiVert"               : makeHeaderInfo(self.__header.data_counts, 5, 0x8, fuiVert), #! 0x60
            "fuiTimelineFrame"      : makeHeaderInfo(self.__header.data_counts, 6, 0x48, fuiTimelineFrame), #! 0x64
            "fuiTimelineEvent"      : makeHeaderInfo(self.__header.data_counts, 7, 0x48, fuiTimelineEvent), #! 0x68
            "fuiTimelineEventName"  : makeHeaderInfo(self.__header.data_counts, 1, 0x40, fuiTimelineEventName), #! 0x50
            "fuiReference"          : makeHeaderInfo(self.__header.data_counts, 8, 0x48, fuiReference), #! 0x6c
            "fuiEdittext"           : makeHeaderInfo(self.__header.data_counts, 9, 0x138, fuiEdittext), #! 0x70
            "fuiFontName"           : makeHeaderInfo(self.__header.data_counts, 13, 0x104, fuiFontName), #! 0x80
            "fuiSymbol"             : makeHeaderInfo(self.__header.data_counts, 10, 0x48, fuiSymbol), #! 0x74
            "fuiImportAsset"        : makeHeaderInfo(self.__header.data_counts, 14, 0x40, fuiImportAsset), #! 0x84
            "fuiBitmap"             : makeHeaderInfo(self.__header.data_counts, 11, 0x20, fuiBitmap), #! 0x78
            "images_size"           : makeHeaderInfo(self.__header.data_counts, 12, 0x1),  #! 0x7c | size of bytes at the end
        }
        #! dictionary containing fuiObject derived classes
        self._parsed_objects:dict = {
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
            "images" : []
        }
        self.__parse_fui_objects()

    def validate_class_size(self, section_name:str, cls) -> bool:
        return self.__HeaderDataInfo[section_name].element_size == struct.calcsize(cls.fmt)

    def is_valid_index(self, section_name:str, index:int) -> bool:
        return -1 < index < self.__HeaderDataInfo[section_name].count

    def validate_content_size(self) -> bool:
        size:int = 0
        for _,hInfo in self.__HeaderDataInfo.items(): size += hInfo.section_size
        return size == self.__header.content_size

    def validate_folder_dest(self, output_path:str) -> str:
        output_path = os.path.join(output_path, f"{self.__header.import_name.replace('.swf','')}")
        try: os.makedirs(output_path)
        #! clear out directory if already exists
        except OSError:
            self.clean(output_path)
        return output_path

    #! TODO: make this robust | folder deletion
    def clean(self, path:str) -> None:
        for root, _, files in os.walk(path):
            for file in files:
                os.remove(os.path.join(root, file))

    def __parse_fui_objects(self) -> None:
        for key,data in self.__HeaderDataInfo.items():
            if data.repr_cls is None: continue
            self.__parse(key, self._parsed_objects[key])
        for bitmap in self.get_bitmaps():
            offset = self.get_start_offset_of("images_size")
            self._parsed_objects["images"].append(self.__get_raw_data(offset + bitmap.offset, bitmap.size))

    def __parse(self, section_name:str, container:list) -> None:
        cls = self.__HeaderDataInfo[section_name].repr_cls
        if not self.validate_class_size(section_name, cls): raise Exception("Class does not contain the required size!")
        for i in range(self.__HeaderDataInfo[section_name].count):
            offset = self.__get_indexed_offset(section_name, i)
            data_size = self.__HeaderDataInfo[section_name].element_size
            container.append(cls(self.__get_raw_data(offset, data_size)))
 
    def __get_raw_data(self, offset:int, size:int) -> bytearray:
        return self.__raw_data[offset:offset+size]

    def __get_indexed_offset(self, section_name:str, index:int = 0) -> int:
        if not self.is_valid_index(section_name, index): raise Exception("Index out of range")
        return self.get_start_offset_of(section_name) + index * self.__HeaderDataInfo[section_name].element_size

    def get_imported_assets(self) -> list:
        return self._parsed_objects["fuiImportAsset"]

    def get_fonts(self) -> list:
        return self._parsed_objects["fuiFontName"]

    def get_symbols(self) -> list:
        return self._parsed_objects["fuiSymbol"]

    def get_timeline_frames(self) -> list:
        return self._parsed_objects["fuiTimelineFrame"]

    def get_timeline_actions(self) -> list:
        return self._parsed_objects["fuiTimelineAction"]

    def get_references(self) -> list:
        return self._parsed_objects["fuiReference"]

    def get_bitmaps(self) -> list:
        return self._parsed_objects["fuiBitmap"]

    def get_timeline_events(self) -> list:
        return self._parsed_objects["fuiTimelineEvent"]

    def get_timeline_event_names(self) -> list:
        return self._parsed_objects["fuiTimelineEventName"]
    
    def get_timelines(self) -> list:
        return self._parsed_objects["fuiTimeline"]

    def get_verts(self) -> list:
        return self._parsed_objects["fuiVert"]

    def get_shapes(self) -> list:
        return self._parsed_objects["fuiShape"]

    def get_shape_components(self) -> list:
        return self._parsed_objects["fuiShapeComponent"]

    def get_edittext(self) -> list:
        return self._parsed_objects["fuiEdittext"]

    def contains_images(self) -> bool:
        return len(self.get_bitmaps()) > 0

    def __decode_image(self, raw_data:bytes | bytearray, read_flags:int = cv2.IMREAD_ANYCOLOR | cv2.IMREAD_UNCHANGED) -> numpy.ndarray:
        data = numpy.asarray(bytearray(raw_data), dtype=numpy.uint8)
        return cv2.imdecode(data, read_flags)

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
        ext = "png" if (bitmap.format == bitmap.eBitmapFormat.JPEG_WITH_ALPHA_DATA or bitmap.format < 6) else "jpeg"
        filename = f"{output_file}.{ext}"
        print("Dumping:", filename[len(os.getcwd()):])
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
            self.__dump_image(f"{os.path.join(output_path, symbol.name)}", bitmap)
            count += 1
        print("Successfully dumped all images!\n" if count == len(bitmaps) else "", end="")

    def dump_raw(self, output_path:str) -> None:
        if not self.contains_images():
            print("This fui file does not contain any images")
            return
        output_path = self.validate_folder_dest(output_path)
        [self.__dump_image(os.path.join(output_path, f"image_{i}"), bitmap) for i,bitmap in enumerate(self.get_bitmaps())]

    def get_start_offset_of(self, section_name:str) -> int:
        if section_name not in self.__HeaderDataInfo.keys() or self.__HeaderDataInfo[section_name].count == 0: return -1
        offset:int = self.__header.header_size
        for key, header_info in self.__HeaderDataInfo.items():
            if key == section_name: return offset
            offset += header_info.section_size
        return -1

    def find(self, name:str) -> list[fuiBitmap] | fuiBitmap | list[fuiTimeline] | fuiTimeline | None:
        results:tuple = ()
        for symbol in self.get_symbols():
            if name.lower() in symbol.name.lower():
                caller, data_type = (self.get_bitmaps, 'fuiBitmap') if symbol.obj_type == eFuiObjectType.BITMAP else (self.get_timelines, 'fuiTimeline')
                data = caller()[symbol.index]
                print(f"{symbol.name} | Offset: {self.__get_indexed_offset(data_type, symbol.index)} | {data}")
                results += (data,)
        if len(results) > 0: return results if len(results) > 1 else results[0]
        print(f"Could not find Symbol named '{name}'")
        return None

    def __str__(self) -> str:
       return self.__header.__str__()