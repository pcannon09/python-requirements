import sys

def getPythonVersion():
    """
    @brief Get the current python version
    This can be used to check if the current python version is available
    """

    if (sys.version_info < (3, 6)):
        print("[ ERR ] This code requires at least Python 3.6")

        sys.exit(1)

