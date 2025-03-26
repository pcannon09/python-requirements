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
        """
        @brief Initalize everything for the parser
        * NOTES:
        ** AVAILABLE FLAGS:
        --ignore-errors # Ignores all the errors
        --no-system-commands # Disable the execution of system commands
        """

        debug.debug(f"Initializing `{id}` with path `{path}` and setting the required variables")
        
        self.path: str = path
        self.id: str = id
        self.spacing = r"\s*" # Equivalent to ' ' ( Space )
        self.quote = r'["\']' # `'` or `"`

        self.installDir: str = ""
        self.confPath: str = ""
        self.osNameReq: str = "any"
        self.platform: str = "any"
        self.pipFlags: str = ""
        self.moduleDirPath: str = "pip_modules/"
        self.flags: list = []

        self.lineNum: int = 0

        self.file = None

        if (path != ""):
            try:
                self.file = open(path, "r")

            except FileNotFoundError:
                print(f"Could not find `{path}` file. Please provide a valid path")

                sys.exit(1)

            if (not os.path.exists(path)):
                print(f"[ ERR ] Path \"{path}\" does not exist, make sure to have a valid path")

                sys.exit(1)

        # Set the commands in the requirements file
        self.commands: list = [
            # {matchCommand}                                              ,                                               {functionCall}
            [r'remove.install_dir', self.remove_installDir], # Remove the previously set installation dir
            [r'remove.conf_dir', self.remove_confDir], # Remove the configuration dir

            [rf'{self.spacing}install{self.spacing}{self.quote}(.*){self.quote}=={self.quote}(.*){self.quote}', self.install], # Install the following package with the specified version
            [rf'{self.spacing}remove{self.spacing}{self.quote}(.*){self.quote}=={self.quote}(.*){self.quote}', self.remove], # Remove the following package with the specified version (Only works with the set installation dir)

            [rf'{self.spacing}install{self.spacing}{self.quote}(.*){self.quote}', self.install], # Install the following package
            [rf'{self.spacing}remove{self.spacing}{self.quote}(.*){self.quote}', self.remove], # Remove the following package

            [rf'\$\{{{self.spacing}(.*){self.spacing}}}', self.runSystemCommand], # Execute system command

            [rf'\[{self.spacing}install_dir{self.spacing}={self.spacing}{self.quote}(.*){self.quote}{self.spacing}\]', self.statement_installDir], # Set install dir
            [rf'\[{self.spacing}required_os{self.spacing}={self.spacing}{self.quote}(.*){self.quote}{self.spacing}\]', self.statement_setRequiredOS], # Set required OS
            [rf'\[{self.spacing}modules_path{self.spacing}={self.spacing}{self.quote}(.*){self.quote}{self.spacing}\]', self.statement_setModulePath], # Set config path
            [rf'\[{self.spacing}conf_dir{self.spacing}={self.spacing}{self.quote}(.*){self.quote}{self.spacing}\]', self.statement_setConfDir], # Set config dir
            [rf'\[{self.spacing}flags{self.spacing}={self.spacing}{self.quote}(.*){self.quote}{self.spacing}\]', self.statement_pipFlags], # Set flags
            [rf'\[{self.spacing}requirements_flags{self.spacing}={self.spacing}{self.quote}(.*){self.quote}{self.spacing}\]', self.statement_requirementsFlag], # Set requirements flags

            [rf'{self.spacing}print{self.spacing}{self.quote}(.*){self.quote}{self.spacing}', self.print] # Print text to the output
        ]

    def print(self, line: str, matching) -> list:
        """
        @brief print something to the output in requirements
        * USAGE:
        print {text}
        """

        if (matching):
            for x in matching.groups():
                print(x)

            return [0, ""]

        return [-1, "No matching command for `print()`"]

    def statement_setModulePath(self, line: str, matching) -> list:
        """
        @brief Set the path of the pip_modules in the configuration file

        * USAGE:
        [ modules_path = "./path/to/pip_modules" ]
        """

        if (matching):
            if (matching.group(1) == self.spacing):
                return [-1, "Configuration path must contain a valid path"]

            self.moduleDirPath = matching.group(1)

            return [0, ""]

        return [-1, "No matching command for `statement_setModulePath()`"]

    def statement_requirementsFlag(self, line: str, matching) -> list:
        """
        @brief Set the flags for the requirements file
        
        * USAGE:
        [ requirements_flags = "{flag1} {flag2} {...}" ]
        """

        if (matching):
            flags: str = matching.group(1)

            self.flags = flags.split(" ")

            return [0, ""]

        return [-1, "No matching command for `statement_requirementsFlag()`"]

    def remove_confDir(self, line: str, matching) -> list:
        """
        @brief Remove the set configuration file

        * USAGE:
        remove.conf_dir
        """

        if (os.path.exists(self.confPath)):
            os.remove(self.confPath)

            return [0, ""]

        return [1, f"Config path `{self.confPath}` does not exist. Make sure to set a valid path"]

    def statement_pipFlags(self, line: str, matching) -> list:
        """
        @brief Set the flags when pip command is executed, the flags are the same as when you pass them to a pip command

        * USAGE:
        [ flags = "{flags}" ]
        """

        if (matching):
            self.pipFlags = matching.group(1)

            return [0, ""]

        return [-1, "No matching command for `statement_pipFlags()`"]

    def statement_setConfDir(self, line: str, matching) -> list:
        """
        @brief Set the configuration dir

        * USAGE:
        [ conf_dir = "./path/to/conf.py" ]
        """

        if (matching):
            if (not os.path.exists(matching.group(1))):
                os.makedirs(os.path.dirname(matching.group(1)), exist_ok=True)

            writeStr: str = f"""# Auto generated config file from `python-requirements`

import sys

sys.path.append("{self.moduleDirPath}") # Add the modules path
"""

            with open(matching.group(1), "w") as f:
                f.write(writeStr)

            self.confPath = matching.group(1)

            return [0, ""]

        return [-1, "No matching command for `statement_setConfDir()`"]

    def statement_setRequiredOS(self, line: str, matching) -> list:
        """
        @brief Set the required OS for installation
        Examples:
        linux,
        darwin,
        windows,
        any

        * USAGE:
        [ required_os = "{OS}" ]
        """

        if (matching):
            self.osNameReq = matching.group(1).lower()

            return [0, ""]

        return [-1, "No matching command for `statement_setRequiredOS()`"]

    def install(self, line: str, matching) -> list:
        """
        @brief Install a module from pip

        * USAGE:
        install "{module}"
        """

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
                    if (len(matching.groups()) <= 2):
                        command = f"pip3 install --target={self.installDir} {matching.group(1)} {self.pipFlags}"

                    else:
                        command = f"pip3 install --target={self.installDir} {matching.group(1)}=={matching.group(2)} {self.pipFlags}"

            commandRun = subprocess.run(command, shell=True)

            return [commandRun.returncode, commandRun.stderr]

        return [-1, "No matching command for `install()`"]

    def remove(self, line: str, matching) -> list:
        """
        @brief Remove a package installed from the modules dir

        * USAGE:
        remove "{module}"
        """

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
        """
        @brief Remove a directory from the matching regex
        """

        if (matching):
            if (os.path.exists(matching.group(1))):
                shutil.rmtree(matching.group(1))

                return [0, ""]

            debug.debug(f"[ WARN ] `{matching.group(1)}` does not exist, hence, not removing it")

        return [-1, "No matching command for `removeDir()`"]

    def runSystemCommand(self, line: str, matching) -> list:
        """
        @brief Run any system command

        * USAGE:
        ${ {command} }
        """

        for flag in self.flags:
            if (flag == "--no-system-commands"):
                return [-1, "Running system commands are not allowed in this configuration"]

        if (matching):
            commandRun = subprocess.run([matching.group(1)], shell=True)

            return [commandRun.returncode, commandRun.stderr]

        return [-1, "No matching command for `runSystemCommand()`"]

    def remove_installDir(self, line: str, matching) -> list:
        """
        @brief Remove previously set installation dir

        * USAGE:
        remove.install_dir
        """

        if (matching):
            if (os.path.exists(self.installDir)):
                shutil.rmtree(self.installDir)

                return [0, ""]

            else:
                return [1, f"No matching path for `{self.installDir}`. Ignoring"]

        return [-1, "No matching command for `remove_installDir()`"]

    def statement_installDir(self, line: str = "", matching: Any = Any) -> list:
        """
        @brief Set the installation dir

        * USAGE:
        [ install_dir = "./path/to/pip_modules" ]
        """

        self.installDir = matching.group(1)

        return [0, ""]

    def parse(self, string: str = "") -> list:
        """
        @brief Parse a string or file to execute the requirements
        """

        lines: str | list = ""

        if (string == ""):
            if (self.file is not None):
                lines = self.file.read().split("\n")

        else:
            lines = string.split("\n")

        for line in lines:
            line = line.strip()

            self.lineNum += 1

            for x in self.commands:
                matching = re.match(x[0], line)

                if (matching):
                    result: list = x[1](line=line, matching=matching)

                    if (result[0] < 0): # Error
                        result[1] += f"\nLINE INFO:\n{self.lineNum} | {line}"
                        
                        ignoreErrs: bool = False

                        for flag in self.flags:
                            if (flag == "--ignore-errors"):
                                ignoreErrs = True

                        if (not ignoreErrs):
                            return result

                        else:
                            print(f"[ ERROR | WARN ] Ignored error:\n{result[0]}\n{result[1]}")
                    
                    elif (result[0] == 1): # Warning
                        print(f"[ WARN ] {result[1]}")

                    break

            else:
                if not line.startswith("#") and line:
                    ignoreErrs: bool = False

                    for flag in self.flags:
                        if (flag == "--ignore-errors"):
                            ignoreErrs = True

                    if (not ignoreErrs):
                        return [-1, f"Unknown command in file `{self.path}` on line `{self.lineNum}`: {line}"]

                    else:
                        print(f"Unknown command in file `{self.path}` on line `{self.lineNum}`: {line}")

        return [0, "Success"]

