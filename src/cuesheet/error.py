from .statement import Statement


class Error:
    def __init__(self, line_number: int, cause: Statement | str):
        self.line_number = line_number
        self.cause = cause
