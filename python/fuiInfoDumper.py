import os, argparse

from fuiParser import fuiParser

def main():
    argvparser = argparse.ArgumentParser()
    argvparser.add_argument("fuiFile", type=str, help="FUI File to be Parsed.")
    argvparser.add_argument("-sym", "--symbols", action="store_true", default=False, help="Prints out all Symbols contained in a file")
    argvparser.add_argument("-d", "--dump", action="store_true", default=False, help="Dumps images(with symbol name) into a folder(default is 'output')")
    #! TODO: impl this
    # argvparser.add_argument("-r", "--replace", metavar=("Bitmap_symbol","image_file"), nargs=2, choices=["img_format"], action="store", default=False, help="Replaces given name with the passed image")
    argvparser.add_argument("-rd","--raw-dump", action="store_true", default=False, help="Dumps all images into a folder(default is 'output')")
    argvparser.add_argument("-f","--find", metavar="name", type=str, action="store", help="Prints out fui Element's that contain [name]")
    argvparser.add_argument("-frefs","--find-references", dest="find_ref", metavar="folder", type=str, action="store", help="Tries to find references contained in Import files")
    parsedagrs = argvparser.parse_args()
    if not parsedagrs.fuiFile.endswith(".fui"): raise Exception("Not a fui file")
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
            parser.find(parsedagrs.find)
        if parsedagrs.symbols:
            print("Symbols:")
            for symbol in parser.get_symbols():
                print(symbol.name)

        if parsedagrs.find_ref:
            if not os.path.exists(parsedagrs.find_ref) or len(parser.get_imported_assets()) == 0: return
            fui_parser = []
            for file in os.listdir(parsedagrs.find_ref):
                if file.endswith(".fui"):
                    abs_path = os.path.join(os.path.abspath(parsedagrs.find_ref),file)
                    with open(abs_path, "rb") as fui:
                        fui_parser.append((file,fuiParser(fui.read())))

            for import_file in parser.get_imported_assets():
                for (file_name, cur_parser) in fui_parser:
                    if cur_parser.header.swf_name == import_file.import_name:
                        print(f"Found import name({import_file.import_name}) in {file_name}")

        # print(f"Imported Assets: {parser.get_imported_assets()}\n")
        # print(f"Symbol Names: {parser.get_symbols()}\n")
        # print(f"Reference Names: {parser.get_references()}\n")
        # print(f"Reference Names: {len(parser.get_references())}\n")

        # print(f"Shapes: {parser.get_shapes()}\n")
        # print(f"Shape Components: {parser.get_shape_components()}\n")

        # print(f"Shape count: {len(parser.get_shapes())}\n")
        # print("Shape Component count:", len(parser.get_shape_components()))

        # print(len(parser.get_timeline_actions()))
        # print(parser.get_start_offset_of("fuiTimelineAction"))

        # parser.print_timeline_tree()
        
        # print(len(parser.get_edittext()))

        # print(f"Font Names: {parser.get_fonts()}\n")
        # print(f"Vert : {parser.get_vert()}\n")
        # print(f"Vert : {len(parser.get_vert())}\n")
        # print(parser.validate_content_size())


if __name__ == "__main__":
    main()