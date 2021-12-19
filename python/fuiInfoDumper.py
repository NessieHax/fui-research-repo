import sys, os

from fuiParser import fuiParser

argc = len(sys.argv)


def usage() -> None:
    print(f"\nUsage: {__file__[len(os.getcwd()):]} <(fui file)> [opt]")
    print(f"Options:\n\t -d, --dump [folder](Optional)\t\tDumps images(with symbol name) into a folder(default is 'output').")
    print(f"\n\t -rd, --raw-dump [folder](Optional)\tDumps all images into a folder(default is 'output').")
    print(f"\n\t -f, --find name\tPrints all images that contain [name].")
    print(f"\n\t -h, --help name\tDisplay this message.")


def main():
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        usage()
        return
    with open(sys.argv[1],"rb") as fui:
        parser = fuiParser(fui.read())
        parser.parse() #! needs to be called before you're able to access data via the getter
        # print(parser.header)
        #! TODO: multi flag support
        if argc > 2:
            output_path = sys.argv[3] if argc > 3 else "output"
            if sys.argv[2] == "--help" or sys.argv[2] == "-h":
                usage()
            elif sys.argv[2] == "--dump" or sys.argv[2] == "-d":
                parser.dump_images(f"{os.getcwd()}/{output_path}")
            elif sys.argv[2] == "--raw-dump" or sys.argv[2] == "-rd":
                parser.dump_raw(f"{os.getcwd()}/{output_path}")
            elif sys.argv[2] == "--find" or sys.argv[2] == "-f" and argc > 3:
                parser.get_image_by_name(sys.argv[3])

        # print(f"Imported Assets: {parser.get_imported_assets()}\n")
        # print(f"Symbol Names: {parser.get_symbols()}\n")
        print(f"Reference Names: {parser.get_references()}\n")

        # print([x for x in parser.get_symbols() if x.obj_type != 3])
        # print([x for x in parser.get_timelines() if x.unkn_0x0 != -1])
        # print([parser.get_timelines()[x.index] for x in parser.get_symbols() if x.obj_type == 2])

        # print(f"Bitmaps: {parser.get_bitmaps()}\n")
        print(f"Shapes: {parser.get_shapes()}\n")
        print("Shape count:", len(parser.get_shapes()))
        print(f"Shape Components: {parser.get_shape_components()}\n")
        print("Shape Component count:", len(parser.get_shape_components()))

        # print(f"Timeline : {parser.get_timelines()}\n")
        # print(f"Timeline Event({len(parser.get_timeline_events())}): {parser.get_timeline_events()}\n")
        # print(f"Timeline Event Names: {parser.get_timeline_event_names()}\n")

        for data in parser.get_timelines():
            print(f"'{parser.get_timeline_frames()[data.frame_name_index].frame_name}' -> {data}")
        print()
        for data in parser.get_timeline_events():
            if data.name_index > -1: print(parser.get_timeline_event_names()[data.name_index].name, ":", data)
        # print(len(parser.get_edittext()))
        # for data in parser.get_edittext():
        #     print(data)

        # print(f"Timeline Frame Names: {parser.get_timeline_frames()}\n")
        # print(f"Timeline Actions: {parser.get_timeline_actions()}\n")
        # print(f"Font Names: {parser.get_fonts()}\n")
        # print(f"Vert : {parser.get_vert()}\n")
        # print(f"Vert : {len(parser.get_vert())}\n")
        # print(parser.validate_content_size())


if __name__ == "__main__" and argc > 1:
    main()
else:
    usage()