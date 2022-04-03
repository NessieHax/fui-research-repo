import sys

from fuiParser import fuiParser

def main():
    parser = fuiParser(sys.argv[1])
    print(parser)


if __name__ == "__main__" and len(sys.argv) > 1:
    main()