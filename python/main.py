from File import File
from Debug import debug

import sys

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        filePath = sys.argv[1]

    else:
        filePath = ".requirements"

    debug.debug(f"Opening `{filePath}`...", "info")

    file: File = File("parse-req-main", filePath)

    debug.debug(f"Parsing `{file.id}`...", "info")

    out = file.parse()

    print(out)

    if (out[0] == 0):
        debug.debug(f"Done parsing `{file.id}`...", "info")

