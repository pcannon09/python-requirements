from File import File
from Debug import debug
from ReqInfo import ReqInfo

import sys
import readline

def outMsg(file: File, out: list):
    if (out[0] == 0):
        debug.debug(f"Done parsing `{file.id}`...", "info")

    elif (out[0] < 0):
        debug.debug(f"Failed to parse `{file.id}`...", "error")

    elif (out[0] == 1):
        debug.debug(f"Warning when parsing `{file.id}`...", "warn")

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

        elif (sys.argv[1] == "--path" or sys.argv[1] == "-p"):
            if (len(sys.argv) > 2):
                filePath = sys.argv[2]

            else:
                print("Parameter `path` was not provided. Please provide a valid path")

                sys.exit(1)

        elif (sys.argv[1] == "--shell" or sys.argv[1] == "-s"):
            line: int = 1
            totalCommand: list = [[line, ""]]
            totalCommandStr: str = ""

            if (len(sys.argv) > 2):
                if (sys.argv[2] != ""):
                    file: File = File("shell-parse-req-main-param", "")
                    out = file.parse(totalCommandStr)

                    print(f"Exit code:    {out[0]}")
                    print(f"Exit message: {out[1]}")

                    outMsg(file, out)

                    sys.exit(0)

            while (1):
                command: str = input(f"{line} >>> ")

                if (command == "EXIT"):
                    break

                elif (command.lower() == "HELP".lower()):
                    print("* HELP")
                    print("Commands:")
                    print("[ HELP ] Show this help")
                    print("[ EXIT ] Exit shell")
                    print("[ RUN ] Run the previous scripts")
                    print("[ RESET ] Clear all the commands and previous scripts")

                    continue

                elif (command == "RUN"):
                    if (len(totalCommandStr) == 0):
                        print("Cannot RUN shell. Make sure you have a script that contains something")

                        continue

                    file: File = File("shell-parse-req-main", "")
                    out = file.parse(totalCommandStr)

                    print(f"Exit code:    {out[0]}")
                    print(f"Exit message: {out[1]}")

                    outMsg(file, out)

                    continue
                
                elif (command == "RESET"):
                    line = 0
                    totalCommandStr = ""
                    totalCommand = [0, ""]

                    continue

                elif (command.split(" ")[0] == "GOTO"):
                    print(f"GOTO L{command.split(" ")[1]}")

                    try:
                        del totalCommand[int(command.split(" ")[1]):]

                    except ValueError:
                        print("[ ERROR ] Please provide an int")

                        continue

                    totalCommandStr = totalCommand[int(command.split(" ")[1])]

                    continue

                line += 1
                totalCommandStr += f"{command}\n"
                totalCommand.append([line, f"{command}\n"])

            sys.exit(0)

    debug.debug(f"Opening `{filePath}`...", "info")

    file: File = File("parse-req-main", filePath)

    debug.debug(f"Parsing `{file.id}`...", "info")

    out = file.parse()

    print(f"Exit code:    {out[0]}")
    print(f"Exit message: {out[1]}")

    outMsg(file, out)

