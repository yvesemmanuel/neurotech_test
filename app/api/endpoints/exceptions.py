'''This module defines custom exceptions used in the API.

Exceptions:
    - `InvalidRequestError`: Raised when a request is invalid or doesn't
        comply with the expected schema.
    - `InternalServerError`: Raised when an unexpected error occurs while processing a request.
    - `InvalidPathError`: Raised when a request path is invalid or not found.
'''


class InvalidRequestError(Exception):
    '''
    Exception raised when a request body is invalid or doesn't match the expected schema.

    Attributes:
        message (str): The explanation of the error.
    '''

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InternalServerError(Exception):
    '''
    Exception raised when an unexpected error occurs in the server.

    Attributes:
        message (str): The explanation of the error.
    '''

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidPathError(Exception):
    '''
    Exception raised when a requested path is invalid.

    Attributes:
        message (str): The explanation of the error.
    '''

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
