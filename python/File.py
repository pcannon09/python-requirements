from Debug import debug

from typing import Any

import os
import re
import shutil
import platform
import subprocess
import glob
import sys

class File:
    def __init__(self, id: str, path: str):
        debug.debug(f"Initializing `{id}` with path `{path}` and setting the required variables")
        
        if (not os.path.exists(path)):
            print(f"[ ERR ] Path \"{path}\" does not exist, make sure to have a valid path")

            sys.exit(1)

        self.path: str = path
        self.id: str = id
        self.spacing = r"\s*" # Equivalent to ' ' ( Space )
        self.quote = r'["\']' # `'` or `"`

        self.installDir: str = ""
        self.confPath: str = ""
        self.osNameReq: str = "any"

        self.lineNum: int = 0

        self.file = open(path, "r")

        self.commands: list = [
            # {matchCommand}                                              ,                                               {functionCall}
            [r'remove.install_dir', self.remove_installDir],

            [rf'{self.spacing}install{self.spacing}{self.quote}(.*){self.quote}=={self.quote}(.*){self.quote}', self.install],
            [rf'{self.spacing}remove{self.spacing}{self.quote}(.*){self.quote}=={self.quote}(.*){self.quote}', self.remove],

            [rf'{self.spacing}install{self.spacing}{self.quote}(.*){self.quote}', self.install],
            [rf'{self.spacing}remove{self.spacing}{self.quote}(.*){self.quote}', self.remove],

            [rf'\$\{{{self.spacing}(.*){self.spacing}}}', self.runSystemCommand],

            [rf'\[{self.spacing}install_dir{self.spacing}={self.spacing}{self.quote}(.*){self.quote}{self.spacing}\]', self.statement_installDir],
            [rf'\[{self.spacing}required_os{self.spacing}={self.spacing}{self.quote}(.*){self.quote}{self.spacing}\]', self.statement_setRequiredOS],
            [rf'\[{self.spacing}conf_dir{self.spacing}={self.spacing}{self.quote}(.*){self.quote}{self.spacing}\]', self.statement_setConfDir]
        ]

    def statement_setConfDir(self, line: str, matching) -> list:
        if (matching):
            if (not os.path.exists(matching.group(1))):
                os.makedirs(os.path.dirname(matching.group(1)), exist_ok=True)

            writeStr: str = f"""
# Auto generated config file from `python-requirements`

import sys

sys.path.append("{self.installDir}") # Add the modules path
"""

            with open(matching.group(1), "w") as f:
                f.write(writeStr)

            self.confPath = matching.group(1)

            return [0, ""]

        return [-1, "No matching command for `statement_setConfDir()`"]

    def statement_setRequiredOS(self, line: str, matching) -> list:
        if (matching):
            self.osNameReq = matching.group(1).lower()

            return [0, ""]

        return [-1, "No matching command for `statement_setRequiredOS()`"]

    def install(self, line: str, matching) -> list:
        command: str = ""

        if (matching):
            if (self.installDir == ""):
                if (platform.system().lower() == self.osNameReq or self.osNameReq.lower() == "any"):
                    if (len(matching.groups()) <= 1):
                        command = f"pip3 install {matching.group(1)} --break-system-packages"

                    else:
                        command = f"pip3 install {matching.group(1)}=={matching.group(2)} --break-system-packages"

            else:
                if (not os.path.exists(self.installDir)):
                    os.makedirs(f"{os.getcwd()}/{self.installDir}")

                if (platform.system().lower() == self.osNameReq or self.osNameReq.lower() == "any"):
                    if (len(matching.groups()) <= 1):
                        command = f"pip3 install --target={self.installDir} {matching.group(1)}"

                    else:
                        command = f"pip3 install --target={self.installDir} {matching.group(1)}=={matching.group(2)}"

            commandRun = subprocess.run(command, shell=True)

            return [commandRun.returncode, commandRun.stderr]

        return [-1, "No matching command for `install()`"]

    def remove(self, line: str, matching) -> list:
        if matching:
            if (self.installDir == ""):
                if (len(matching.groups()) > 1):
                    return [-1, "The equality operator (==) in the `remove` command can only be used when `install_dir` is set"]

                command = f"pip3 uninstall {matching.group(1)} --break-system-packages"

                commandRun = subprocess.run([command], shell=True)

                return [commandRun.returncode, commandRun.stderr]

            else:
                if (len(matching.groups()) < 1):
                    removeDirStr = rf"{self.installDir}*{matching.group(1)}*"

                else:
                    removeDirStr = rf"{self.installDir}*{matching.group(1)}*{matching.group(2)}*"

                matchingDirs = glob.glob(removeDirStr)

                for path in matchingDirs:
                    if (os.path.exists(path)):
                        shutil.rmtree(f"{path}")

                pythonIncFile = f"{self.installDir}include/python/{matching.group(1)}"

                if (os.path.exists(pythonIncFile)):
                    shutil.rmtree(pythonIncFile)

                return [0, ""]

        return [-1, "No matching command for `remove()`"]

    def removeDir(self, line: str, matching) -> list:
        if (matching):
            if (os.path.exists(matching.group(1))):
                shutil.rmtree(matching.group(1))

                return [0, ""]

            debug.debug(f"[ WARN ] `{matching.group(1)}` does not exist, hence, not removing it")

        return [-1, "No matching command for `removeDir()`"]

    def runSystemCommand(self, line: str, matching) -> list:
        if (matching):
            commandRun = subprocess.run([matching.group(1)], shell=True)

            return [commandRun.returncode, commandRun.stderr]

        return [-1, "No matching command for `runSystemCommand()`"]

    def remove_installDir(self, line: str, matching) -> list:
        if (matching):
            if (os.path.exists(self.installDir)):
                shutil.rmtree(self.installDir)

                return [0, ""]

        return [-1, "No matching command for `remove_installDir()`"]

    def statement_installDir(self, line: str = "", matching: Any = Any) -> list:
        self.installDir = matching.group(1)

        return [0, ""]

    def parse(self) -> list:
        lines = self.file.read().split("\n")

        for line in lines:
            line = line.strip()

            self.lineNum += 1

            for x in self.commands:
                matching = re.match(x[0], line)

                if (matching):
                    result = x[1](line=line, matching=matching)

                    if (result[0] != 0):
                        return result

                    break

            else:
                if not line.startswith("#") and line:
                    return [-1, f"Unknown command in file `{self.path}` on line `{self.lineNum}`: {line}"]

        return [0, "Success"]

