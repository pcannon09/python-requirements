from ReqInfo import ReqInfo
import datetime as dt

class Debug:
    save_defaultType: str = "debug"

    def __init__(self, saveFile: str | None, defaultType: str | None = "debug"):
        global save_defaultType

        self.saveFile = saveFile
        self.defaultType = defaultType

        save_defaultType = defaultType

    def debug(self, msg: str, debType: str = save_defaultType):
        debugData = f"[ {dt.datetime.now()} | {debType.capitalize()} ] {msg}"

        if (ReqInfo.DEV):
            print(f"{debugData}")

        if (self.saveFile is not None):
            with open(self.saveFile, "a") as file:
                file.write(f"{debugData}\n")
                file.flush()

if (ReqInfo.DEV):
    debug = Debug(".private/logs/debug.log")

else:
    debug = Debug(None)

