import sys, os

from fuiParser import fuiParser

argc = len(sys.argv)


def usage() -> None:
    print(f"\nUsage: {__file__[len(os.getcwd()):]} <(fui file)> [opt]")
    print(f"Options:\n\t -d, --dump [folder](Optional)\t\tDumps images(with symbol name) into a folder(default is 'output').")
    print(f"\n\t -rd, --raw-dump [folder](Optional)\tDumps all images into a folder(default is 'output').")
    print(f"\n\t -f, --find name\tPrints all images that contain [name].")
    print(f"\n\t -h, --help\tDisplay this message.")


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




if __name__ == "__main__" and argc > 1:
    main()
else:
    usage()