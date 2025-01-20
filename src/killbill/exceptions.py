class KillBillError(Exception):
    """Raised when the Kill Bill API returns an error"""

    def __init__(self, msg: object) -> None:
        super().__init__(msg)


class UnknownError(KillBillError):
    def __init__(self, msg: object = None) -> None:
        if msg is None:
            msg = "Unknown Error"
        super().__init__(msg)


class AuthError(Exception):
    def __init__(self, msg: object = None) -> None:
        if msg is None:
            msg = "Unauthorized"
        super().__init__(msg)


class NotFoundError(Exception):
    def __init__(self, msg: object = None) -> None:
        if msg is None:
            msg = "Source Not Found"
        super().__init__(msg)


class BadRequestError(Exception):
    def __init__(self, msg: object = None) -> None:
        if msg is None:
            msg = "Bad Request"
        super().__init__(msg)
