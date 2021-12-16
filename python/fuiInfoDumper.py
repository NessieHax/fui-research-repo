import sys, os

from fuiParser import fuiParser

argc = len(sys.argv)

def main():
    with open(sys.argv[1],"rb") as fui:
        parser = fuiParser(fui.read())
        parser.parse() #! needs to be called before you're able to access data via the getter
        # print(parser.header)

        # print(f"Imported Assets: {parser.get_imported_assets()}\n")
        # print(f"Symbol Names: {parser.get_symbols()}\n")
        # print([x for x in parser.get_symbols() if x.obj_type != 3])
        # print(f"Bitmaps: {parser.get_bitmaps()}\n")
        # print(f"Shapes: {parser.get_shapes()}\n")
        # print(f"Shape Components: {parser.get_shape_components()}\n")
        # print("Shape count:", len(parser.get_shapes()))
        # print("Shape Component count:", parser.HeaderDataInfo["fuiShapeComponent"].count)
        # print(f"Timeline Event Names: {parser.get_timeline_event()}\n")
        # print(f"Timeline : {parser.get_timelines()}\n")
        # print(f"Timeline Frame Names: {parser.get_timeline_frames()}\n")
        # print(f"Timeline Actions: {parser.get_timeline_actions()}\n")
        # print(f"Reference Names: {parser.get_references()}\n")
        # print(f"Font Names: {parser.get_fonts()}\n")
        # print(f"Vert : {parser.get_vert()}\n")
        # print(parser.validate_content_size())

        output_path = "output"
        parser.get_images(f"{os.getcwd()}/{output_path}")

def usage() -> None:
    print(f"\n\tUsage: {__file__[len(os.getcwd()):]} <(fui file)>\n")

if __name__ == "__main__" and argc > 1:
    main()
else:
    usage()