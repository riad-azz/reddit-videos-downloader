from werkzeug.exceptions import HTTPException


class BadRequest(HTTPException):
    def __init__(self, message):
        self.code = 400
        self.description = message
        super().__init__()


class ServerError(HTTPException):
    def __init__(self, message):
        self.code = 500
        self.description = message
        super().__init__()
