import sys, os

from fuiParser import fuiParser

def main():
    with open(sys.argv[1],"rb") as fui:
        parser = fuiParser(fui.read())
        print(parser.header)
        print(parser)


if __name__ == "__main__" and len(sys.argv) > 1:
    main()