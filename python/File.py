from Debug import debug

from typing import Any

import os
import re
import shutil
import platform
import subprocess
import glob

class File:
    def __init__(self, id: str, path: str):
        debug.debug(f"Initializing `{id}` with path `{path}` and setting the required variables")
        
        if (not os.path.exists(path)):
            print(f"[ ERR ] Path \"{path}\" does not exist, make sure to have a valid path")

            return

        self.path: str = path
        self.id: str = id
        self.installDir: str = ""
        self.spacing = r"\s*" # Equivalent to ' ' ( Space )
        self.quote = r'["\']' # `'` or `"`

        self.lineNum: int = 0

        self.file = open(path, "r")

        self.commands: list = [
            # {matchCommand}                          ,                          {functionCall}
            [rf'{self.spacing}install{self.spacing}{self.quote}(.*){self.quote}', self.install],
            [rf'{self.spacing}remove{self.spacing}{self.quote}(.*){self.quote}', self.remove],
            [rf'\[{self.spacing}install_dir{self.spacing}={self.spacing}{self.quote}(.*){self.quote}{self.spacing}\]', self.statement_installDir],
            [r'\$\{(.*)}', self.runSystemCommand],
            [r'remove.install_dir', self.remove_installDir]
        ]

    def install(self, line: str, matching) -> list:
        global command

        if (matching):
            if (self.installDir == ""):
                command = f"pip3 install {matching.group(1)} --break-system-packages"

            else:
                if (not os.path.exists(self.installDir)):
                    os.makedirs(f"{os.getcwd()}/{self.installDir}")

                command = f"pip3 install --target={self.installDir} {matching.group(1)}"

            commandRun = subprocess.run(command, shell=True)

            return [commandRun.returncode, commandRun.stderr]

        return [-1, "No matching command for `install()`"]

    def remove(self, line: str, matching) -> list:
        if matching:
            if (self.installDir == ""):
                command = f"pip3 uninstall {matching.group(1)} --break-system-packages"

                commandRun = subprocess.run([command], shell=True)

                return [commandRun.returncode, commandRun.stderr]

            else:
                removeDirStr = rf"{self.installDir}*{matching.group(1)}*"
                matchingDirs = glob.glob(removeDirStr)

                for path in matchingDirs:
                    if (os.path.exists(path)):
                        shutil.rmtree(path)

                        os.system("ls ./tests/pip_modules")

                pythonIncFile = f"{self.installDir}include/python/{matching.group(1)}"

                if (os.path.exists(pythonIncFile)):
                    shutil.rmtree(pythonIncFile)

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
                    x[1](line=line, matching=matching)

                    break

            else:
                if not line.startswith("#") and line:
                    return [-1, f"Unknown command in file `{self.path}` on line `{self.lineNum}`: {line}\nExit status -1"]

        return [0, ""]

