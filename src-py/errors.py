from position import Position


class Error:
    def __init__(self, start: Position, end: Position, message: str) -> None:
        self.start: Position = start
        self.end: Position = end
        self.message: str = message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}\nFile: {self.start.fn}, line: {self.start.line_num + 1}"


class InvalidCharError(Error): ...


class InvalidSyntaxError(Error): ...


class RuntimeError(Error): ...
