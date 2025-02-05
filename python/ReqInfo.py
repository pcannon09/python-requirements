class ReqInfo:
    VERSION_MAJOR: int = 0
    VERSION_MINOR: int = 0
    VERSION_PATCH: int = 0

    VERSION_STATE: str = "dev"

    VERSION_TOTAL: str = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"

    DEV: bool = True
