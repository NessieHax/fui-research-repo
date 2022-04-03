import os, argparse, cv2

from fuiParser import fuiParser
from fuiDataStructures.fuiTimeline import fuiTimeline
from fuiDataStructures.fuiShape import fuiShape
from fuiDataStructures.fuiObject import eFuiObjectType
from fuiBuilder import fuiBuilder

def print_timeline_tree(parser:fuiParser, timeline:fuiTimeline, prefix:str = "") -> None:
        print(f"->", timeline)
        for frame in parser.get_timeline_frames()[timeline.frame_index:timeline.frame_index + timeline.frame_count]:
            print(f"{prefix}-->", frame)
            for evnt in parser.get_timeline_events()[frame.event_index:frame.event_index + frame.event_count]:
                print(f"{prefix}---",end="")
                print(">", parser.get_timeline_event_names()[evnt.name_index].name if evnt.name_index > -1 else "Unknown",end=" ")
                print(evnt)
                print(f"{prefix}----",end="")
                if evnt.obj_type == eFuiObjectType.SHAPE and parser.is_valid_index("fuiShape", evnt.index):
                    print_shapes(parser, parser.get_shapes()[evnt.index], prefix+"----")
                if evnt.obj_type == eFuiObjectType.REFERENCE:
                    print(">", parser.get_references()[evnt.index])
                if evnt.obj_type == eFuiObjectType.TIMELINE:
                    print_timeline_tree(parser, parser.get_timelines()[evnt.index], prefix+"----")
                if evnt.obj_type == eFuiObjectType.BITMAP:
                    print(">", parser.get_bitmaps()[evnt.index])
                if evnt.obj_type == eFuiObjectType.EDITTEXT:
                    print(">", parser.get_edittext()[evnt.index])
            print()
            for act in parser.get_timeline_actions()[timeline.action_index:timeline.action_index + timeline.action_count]:
                print(f"{prefix}-->", act)

def print_shapes(parser:fuiParser, shape:fuiShape, prefix:str = "") -> None:
    print(">", shape)
    for component in parser.get_shape_components()[shape.component_index:shape.component_index+shape.component_count]:
        print(f"{prefix}->", component)
        for vert in parser.get_verts()[component.vert_index:component.vert_index+component.vert_count]:
            print(f"{prefix}-->", vert)
        print()

def print_all_timeline_trees(parser:fuiParser) -> None:
    for symbol in parser.get_symbols():
        if symbol.obj_type != eFuiObjectType.TIMELINE: continue
        print(symbol.name)
        data = parser.get_timelines()[symbol.index]
        print_timeline_tree(parser, data)

def main():
    argvparser = argparse.ArgumentParser()
    argvparser.add_argument("fuiFile", type=str, help="FUI File to be Parsed.")
    argvparser.add_argument("-sym", "--symbols", action="store_true", default=False, help="Prints out all Symbols contained in a file")
    argvparser.add_argument("-d", "--dump", action="store_true", default=False, help="Dumps images(with symbol name) into a folder")
    # argvparser.add_argument("-b", "--build", action="store_true", default=False, help="(Re)Builds the fui file")
    argvparser.add_argument("-tree", action="store_true", default=False, help="DEBUG")
    argvparser.add_argument("-l", "--list", action="store", type=str, metavar="fuiObjectType", default=None, help="Lists a given fuiObject list contained in the fui")
    argvparser.add_argument("-o", "--output", action="store", type=str, default="dump_output", help="sets the output path")
    argvparser.add_argument("-b-out", "--build-output", action="store", type=str, default="mod_output", help="sets the output path for the building process")
    argvparser.add_argument("-r", "--replace", metavar=("Bitmap_name", "image_filename"), type=str, nargs=2, action="append", help="Replaces given index with the passed image")
    argvparser.add_argument("-rd","--raw-dump", action="store_true", default=False, help="Dumps all images into a folder")
    argvparser.add_argument("-f","--find", metavar="name", type=str, action="store", help="Prints out fui Element's that contain [name]")
    argvparser.add_argument("-frefs","--find-references", dest="find_ref", metavar="folder", type=str, action="store", help="Tries to find references contained in Import files")
    parsedargs = argvparser.parse_args()
    if not parsedargs.fuiFile.endswith(".fui"): raise Exception("Not a fui file")
    output_path = os.path.abspath(parsedargs.output)

    parser = fuiParser(parsedargs.fuiFile)
    print(parser)

    if parsedargs.dump:
        parser.dump_images(output_path)
    elif parsedargs.raw_dump:
        parser.dump_raw(output_path)
    if parsedargs.find:
        parser.find(parsedargs.find)

    if parsedargs.list is not None:
        if parsedargs.list in parser._parsed_objects.keys():
            print(f"-----{parsedargs.list}-----")
            [print(val) for val in parser._parsed_objects[parsedargs.list]]
            print("File offset:", parser.get_start_offset_of(parsedargs.list))
            print(f"-----{'-'*len(parsedargs.list)}-----\n")
        else:
            print(f"Invalid argument passed\nvalid arguments:\n{parser._parsed_objects.keys()}")

    if parsedargs.symbols:
        print("Symbols:")
        for symbol in parser.get_symbols():
            print("Type:", symbol.obj_type, "Name:", symbol.name)

    if parsedargs.tree:
        print_all_timeline_trees(parser)

    #! this is disgusting
    if parsedargs.find_ref and os.path.exists(parsedargs.find_ref) and len(parser.get_imported_assets()) > 0:
        fui_parser = []
        for file in os.listdir(parsedargs.find_ref):
            if file.endswith(".fui"):
                abs_path = os.path.join(os.path.abspath(parsedargs.find_ref),file)
                with open(abs_path, "rb") as fui:
                    fui_parser.append((file,fuiParser(fui.read())))

        for import_file in parser.get_imported_assets():
            for (file_name, cur_parser) in fui_parser:
                if cur_parser.header.import_name == import_file.import_name:
                    print(f"Found import name({import_file.import_name}) in {file_name}")

    if parsedargs.replace:
        for replace_arg in parsedargs.replace:
            name = replace_arg[0]
            img_filename = os.path.abspath(replace_arg[1])
            index = -1
            for symbol in parser.get_symbols():
                if name == symbol.name and symbol.obj_type == eFuiObjectType.BITMAP:
                    index = symbol.index
            if index == -1:
                print(f"Could not find Bitmap named '{name}'")
                return
            with open(os.path.abspath(img_filename), "rb") as img:
                img_data = img.read()

            parser.replace_bitmap(index, img_data)
        builder = fuiBuilder()
        builder.build_from_parser(parser)

    # print(parser.validate_content_size())

if __name__ == "__main__":
    main()