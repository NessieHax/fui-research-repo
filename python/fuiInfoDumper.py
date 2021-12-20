import os, argparse

from fuiParser import fuiParser

def main():
    argvparser = argparse.ArgumentParser()
    argvparser.add_argument("fuiFile", type=str, help="FUI File to parse.")
    argvparser.add_argument("-d", "--dump", action="store_true", default=False, help="Dumps images(with symbol name) into a folder(default is 'output')")
    argvparser.add_argument("-rd","--raw-dump", action="store_true", default=False, help="Dumps all images into a folder(default is 'output')")
    argvparser.add_argument("-f","--find", metavar="name", type=str, action="store", help="Prints out fuiBitmap's that contain [name]")
    parsedagrs = argvparser.parse_args()
    with open(parsedagrs.fuiFile,"rb") as fui:
        parser = fuiParser(fui.read())
        parser.parse() #! needs to be called before you're able to access data via the getter
        print(parser.header)
        output_path = "output"
        if parsedagrs.dump:
            parser.dump_images(f"{os.getcwd()}/{output_path}")
        if parsedagrs.raw_dump:
            parser.dump_raw(f"{os.getcwd()}/{output_path}")
        if parsedagrs.find:
            parser.get_image_by_name(parsedagrs.find)

        print(f"Imported Assets: {parser.get_imported_assets()}\n")
        # print(f"Symbol Names: {parser.get_symbols()}\n")
        print(f"Reference Names: {parser.get_references()}\n")

        # print([(i, x) for i,x in enumerate(parser.get_symbols()) if x.obj_type != 3])

        # print(f"Shapes: {parser.get_shapes()}\n")
        # print(f"Shape Components: {parser.get_shape_components()}\n")

        print("Shape count:", len(parser.get_shapes()))
        print("Shape Component count:", len(parser.get_shape_components()))

        parser.print_timeline_tree()
        
        # print(parser.get_edittext())
        # print(len(parser.get_timeline_events()))
        # for data in parser.get_timeline_events():
        #     print(data)

        # print(f"Font Names: {parser.get_fonts()}\n")
        # print(f"Vert : {parser.get_vert()}\n")
        # print(f"Vert : {len(parser.get_vert())}\n")
        # print(parser.validate_content_size())


if __name__ == "__main__":
    main()