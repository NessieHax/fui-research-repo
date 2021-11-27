import sys, os

from fuiParser import fuiParser

argc = len(sys.argv)

def main():
    with open(sys.argv[1],"rb") as fui:
        parser = fuiParser(fui.read())
        # print(parser.header)
        if argc > 2: 
            name:str = sys.argv[2]
            if name in parser.HeaderDataInfo.keys():
                print(f"\nOffset start of '{name}' -> {parser.get_start_offset_of(name)} (decimal) | Count: {parser.HeaderDataInfo[name].count}\n")
            else: print(f"Unknown type: '{name}'")

        # print(f"Imported Assets: {parser.get_imported_assets()}\n")
        # print(f"Symbol Names: {parser.get_symbols()}\n")
        # print(f"Timeline Event Names: {parser.get_timeline_events()}\n")
        # print(f"Timeline Frame Names: {parser.get_timeline_frames()}\n")
        # print(f"Timeline Actions: {parser.get_timeline_actions()}\n")
        # print(f"Reference Names: {parser.get_references()}\n")
        # print(f"Font Names: {parser.get_fonts()}\n")
        # print(parser.get_cluster_size())

        # output_path = "output"
        # try: os.makedirs(output_path)
        # #! clears our directory if Already exists
        # except OSError: 
        #     for root, dirs, files in os.walk(output_path):
        #         for file in files:
        #             os.remove(os.path.join(root, file))
        # parser.get_images(f"{os.getcwd()}/output")

if __name__ == "__main__" and argc > 1:
    main()