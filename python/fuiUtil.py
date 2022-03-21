import cv2, numpy, zlib
from typing import Union

from fuiDataStructures.fuiBitmap import fuiBitmap

def decode_image(raw_data:Union[bytes, bytearray], read_flags:int = cv2.IMREAD_ANYCOLOR | cv2.IMREAD_UNCHANGED) -> numpy.ndarray:
    data = numpy.asarray(bytearray(raw_data), dtype=numpy.uint8)
    return cv2.imdecode(data, read_flags)

def get_zlib_buf_size(bitmap:fuiBitmap) -> int:
    return bitmap.size - bitmap.zlib_data_start if bitmap.zlib_data_start > 0 else -1

#! TODO
def get_compressed_zlib_data(data:Union[bytes, bytearray], zlib_start:int, zlib_buf_size:int) -> bytes:
    if zlib_start == 0 or zlib_buf_size == 0:
        print("zlib start or buffer size is NULL")
        return bytes(0)
    return data[zlib_start:zlib_start+zlib_buf_size]

def swap_image_data(img:numpy.ndarray, mode:str = "fui_in") -> numpy.ndarray:
    if mode == "fui_in":
        return cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
    elif mode == "fui_out":
        return cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    raise IOError("Invalid mode.")

def insert_zlib_alpha_channel_data(img:numpy.ndarray, compressed_zlib_data:Union[bytes, bytearray], zlib_buf_size:int) -> numpy.ndarray:
        output = zlib.decompress(compressed_zlib_data, 0, zlib_buf_size)
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
        return img