from io import BufferedReader
import os, cv2

from fuiDataStructures.fuiHeader import fuiHeader
from fuiDataStructures.fuiObject import eFuiObjectType
from fuiDataStructures.fuiBitmap import fuiBitmap
from fuiDataStructures.fuiTimeline import fuiTimeline
from fuiUtil import get_zlib_buf_size, insert_zlib_alpha_channel_data, decode_image, swap_image_data
from fuiFile import fuiFile

class FUIParserError(Exception): ...

class fuiParser:
    def __init__(self, data: BufferedReader):
        self._fui = fuiFile()
        self._fui.parse(data)

    def validate_folder_dest(self, output_path:str) -> str:
        output_path = os.path.join(output_path, f"{self._fui.header.import_name.removesuffix('.swf')}")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        return output_path

    def get_header(self) -> fuiHeader:
        return self._fui.header

    def get_imported_assets(self) -> list:
        return self._fui.import_assets

    def get_font_names(self) -> list:
        return self._fui.font_names

    #! EXISTING string editing is not recommented due to not being sure if it could mess up the classes that init with it
    def get_symbols(self) -> list:
        return self._fui.symbols

    def get_timeline_frames(self) -> list:
        return self._fui.timeline_frames

    def get_timeline_actions(self) -> list:
        return self._fui.timeline_actions

    def get_references(self) -> list:
        return self._fui.references

    def get_bitmaps(self) -> list:
        return self._fui.bitmaps

    def get_timeline_events(self) -> list:
        return self._fui.timeline_events

    def get_timeline_event_names(self) -> list:
        return self._fui.timeline_event_names
    
    def get_timelines(self) -> list:
        return self._fui.timelines

    def get_verts(self) -> list:
        return self._fui.verts

    def get_shapes(self) -> list:
        return self._fui.shapes

    def get_shape_components(self) -> list:
        return self._fui.shape_components

    def get_edittext(self) -> list:
        return self._fui.edittexts

    def contains_images(self) -> bool:
        return len(self.get_bitmaps()) > 0

    def __dump_image(self, output_file:str, bitmap: fuiBitmap, img: bytes) -> None:
        data = img
        ext, write_flags = ("png", [cv2.IMWRITE_PNG_COMPRESSION]) if (bitmap.format == bitmap.eFuiBitmapType.JPEG_WITH_ALPHA_DATA or bitmap.format < 6) else ("jpeg", [cv2.IMWRITE_JPEG_QUALITY])
        filename = f"{output_file}.{ext}"
        print("Dumping:", filename[len(os.getcwd()):])
        img = decode_image(data)
        final_image = img
        if bitmap.format == fuiBitmap.eFuiBitmapType.JPEG_WITH_ALPHA_DATA:
            final_image = cv2.cvtColor(final_image, cv2.COLOR_RGB2RGBA) #! create alpha channel
            zlib_buf_sz = get_zlib_buf_size(bitmap)
            zlib_data =  data[bitmap.zlib_data_start:]
            final_image = insert_zlib_alpha_channel_data(final_image, zlib_data, zlib_buf_sz)
        elif bitmap.format < 6:
            final_image = swap_image_data(img, "fui_out")

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
            self.__dump_image(f"{os.path.join(output_path, symbol.name)}", bitmap, self._fui.images[symbol.index])
            count += 1
        print("Successfully dumped all images!\n" if count == len(bitmaps) else "", end="")

    def dump_raw(self, output_path:str) -> None:
        if not self.contains_images():
            print("This fui file does not contain any images")
            return
        output_path = self.validate_folder_dest(output_path)
        [self.__dump_image(os.path.join(output_path, f"image_{i}"), bitmap, self._fui.images[i]) for i, bitmap in enumerate(self.get_bitmaps())]

    def replace_bitmap(self, index:int, img_data:bytes, img_type:fuiBitmap.eFuiBitmapType = fuiBitmap.eFuiBitmapType.PNG_WITH_ALPHA_DATA) -> None:
        if not self.is_valid_index("fuiBitmap", index):
            raise IndexError("Invalid Index")

        target_bitmap:fuiBitmap = self.get_bitmaps()[index]

        tmp_img_data = decode_image(img_data)
        if img_type == fuiBitmap.eFuiBitmapType.PNG_NO_ALPHA_DATA or img_type == fuiBitmap.eFuiBitmapType.PNG_WITH_ALPHA_DATA:
            tmp_img_data = swap_image_data(tmp_img_data)
        final_img_data:bytearray = bytearray(cv2.imencode(".png", tmp_img_data)[1].tobytes())

        height, width = tmp_img_data.shape[:2]
        target_bitmap.width = width
        target_bitmap.height = height
        old_img_size = target_bitmap.size
        new_img_size = len(final_img_data)

        offset_diff = new_img_size - old_img_size
        print("old", old_img_size)
        print("new", new_img_size)
        print(offset_diff)
        target_bitmap.size = new_img_size

        self._parsed_objects["images"][index] = final_img_data
        
        for bitmap in self.get_bitmaps()[index+1:]:
            bitmap.offset += offset_diff

        self.__header.content_size += offset_diff
        print(f"Successfully changed '{self.get_symbols()[bitmap.symbol_index]}'")

    def find(self, name:str) -> tuple[fuiBitmap | fuiTimeline] | None:
        results:tuple = ()
        for symbol in self.get_symbols():
            if name.lower() in symbol.name.lower():
                caller, data_type = (self.get_bitmaps, 'fuiBitmap') if symbol.obj_type == eFuiObjectType.BITMAP else (self.get_timelines, 'fuiTimeline')
                data = caller()[symbol.index]
                print(f"{symbol.name} | Offset: {'TODO'} | {data}")
                results += (data,)
        if len(results) > 0: return results
        raise FUIParserError(f"Could not find Symbol named '{name}'")

    def __str__(self) -> str:
       return self._fui.header.__str__()