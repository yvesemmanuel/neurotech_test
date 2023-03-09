class InvalidRequestError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InternalServerError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidPathError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
