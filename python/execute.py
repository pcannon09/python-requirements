from File import File
from Debug import debug
from ReqInfo import ReqInfo

import sys

def main():
    filePath: str = ".requirements"

    if (len(sys.argv) > 1):
        if (sys.argv[1] == "--version" or sys.argv[1] == "-v"):
            print(f"python-requirements version: {ReqInfo.VERSION[0]}.{ReqInfo.VERSION[1]}.{ReqInfo.VERSION[2]} {ReqInfo.VERSION[3]}")

            sys.exit(0)

        elif (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
            print("* HELP")
            print("[ --help | -h ] Display this help")
            print("[ --version | -v ] Display version information")
            print("[ --path ] Set the path to provide the requirements")

            sys.exit(0)

        elif (sys.argv[1] == "--path"):
            if (len(sys.argv) > 2):
                filePath = sys.argv[2]

            else:
                print("Parameter `path` was not provided. Please provide a valid path")

                sys.exit(1)

    debug.debug(f"Opening `{filePath}`...", "info")

    file: File = File("parse-req-main", filePath)

    debug.debug(f"Parsing `{file.id}`...", "info")

    out = file.parse()

    print(f"Exit code:    {out[0]}")
    print(f"Exit message: {out[1]}")

    if (out[0] == 0):
        debug.debug(f"Done parsing `{file.id}`...", "info")

    elif (out[0] < 0):
        debug.debug(f"Failed to parse `{file.id}`...", "error")

    elif (out[0] == 1):
        debug.debug(f"Warning when parsing `{file.id}`...", "warn")

