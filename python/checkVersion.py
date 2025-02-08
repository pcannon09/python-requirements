import sys

def getPythonVersion():
    if (sys.version_info < (3, 6)):
        print("[ ERR ] This code requires at least Python 3.6")

        sys.exit(1)

