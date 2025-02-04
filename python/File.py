from Debug import debug

import os
import re

class File:
    def __init__(self, id: str, path: str):
        debug.debug(f"Initializing `{id}` with path `{path}` and setting the required variables")
        
        if (not os.path.exists(path)):
            print(f"[ ERR ] Path \"{path}\" does not exist, make sure to have a valid path")

            return

        self.path: str = path
        self.id: str = id
        self.installDir: str = ""

        self.file = open(path, "r")

    def install(self, line: str):
        global command

        matchCommand = r'remove "(.*)"'

        matching = re.match(matchCommand , line)

        if matching:
            if (self.installDir == ""):
                command = f"pip3 install {matching.group(1)} --break-system-packages"
            
            else:
                if (not os.path.exists(self.installDir)):
                    os.makedirs(f"{os.getcwd()}/{self.installDir}")

                command = f"pip3 install --target={self.installDir} {matching.group(1)}"

            os.system(command)

        else:
            debug.debug(f'Did not match any command that contains `{matchCommand}`', "warn")

    def remove(self, line: str):
        global command

        matchCommand = r'remove "(.*)"'

        matching = re.match(matchCommand, line)

        if matching:
            command = f"pip3 uninstall {matching.group(1)} --break-system-packages"

            os.system(command)

        else:
            debug.debug(f'Did not match any command that contains `{matchCommand}`', "warn")

    def statement_installDir(self, matching):
        self.installDir = matching.group(1)

    def parse(self):
        lines = self.file.read().split("\n")

        for line in lines:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            # Commands
            elif line.startswith("install "):
                self.install(line)

            elif line.startswith("remove"):
                self.remove(line)

            # Command statements
            # elif line.startswith("[") and line.endswith("]"):
            #     matching = re.match(r'install_dir="(.*)"', line)
            #     
            #     if (matching):
            #         self.statement_installDir(matching, line)

            #         return
                
                # matching = re.match()

