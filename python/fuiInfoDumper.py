import struct
import sys, os

from fuiParser import fuiParser
from fuiDataStructures.fuiImportAsset import fuiImportAsset

argc = len(sys.argv)

def main():
    with open(sys.argv[1],"rb") as fui:
        parser = fuiParser(fui.read())
        # print(parser)

        # print(f"Imported Assets: {parser.get_imported_assets()}\n")
        # print(f"Symbol Names: {parser.get_symbols()}\n")    
        # print(f"Timeline Event Names: {parser.get_timeline_event()}\n")
        # print(f"Timeline : {parser.get_timeline_data()}\n")
        # print(f"Timeline Frame Names: {parser.get_timeline_frames()}\n")
        # print(f"Timeline Actions: {parser.get_timeline_actions()}\n")
        # print(f"Reference Names: {parser.get_references()}\n")
        # print(f"Font Names: {parser.get_fonts()}\n")
        print(f"Vert : {parser.get_vert()}\n")
        # print(parser.validate_content_size())

        # output_path = "output"
        # try: os.makedirs(output_path)
        # #! clears out directory if already exists
        # except OSError: 
        #     for root, dirs, files in os.walk(output_path):
        #         for file in files:
        #             os.remove(os.path.join(root, file))
        # parser.get_images(f"{os.getcwd()}/output")

def usage() -> None:
    print(f"\n\tUsage: {__file__[len(os.getcwd()):]} <(fui file)>\n")

if __name__ == "__main__" and argc > 1:
    main()
else:
    usage()