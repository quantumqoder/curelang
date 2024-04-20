from typing import Optional, Self


class Position:
    def __init__(
        self,
        idx: int,
        ln: int,
        col: int,
        fn: str,
        ftxt: str,
    ) -> None:
        self.index = idx
        self.line_num = ln
        self.column_num = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char: Optional[str] = None) -> Self:
        self.index += 1
        self.column_num += 1
        if current_char == "\n":
            self.line_num += 1
            self.column_num = 0
        return self

    def copy(self) -> Self:
        return Position(
            self.index,
            self.line_num,
            self.column_num,
            self.fn,
            self.ftxt,
        )

    def __str__(self) -> str:
        return f"{self.fn=}, {self.line_num=}, {self.column_num=}"
