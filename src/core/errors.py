from typing import Optional

from core.context import Context
from core.position import Position


class Error:
    def __init__(
        self,
        start: Position,
        end: Position,
        message: str,
        context: Optional[Context] = None,
    ) -> None:
        self.start: Position = start
        self.end: Position = end
        self.message: str = message
        self.context: Optional[Context] = context

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}\nFile: {self.start.fn}, line: {self.start.line_num + 1}"


class InvalidCharError(Error): ...


class InvalidSyntaxError(Error): ...


class RuntimeError(Error):
    def __repr__(self) -> str:
        return f"{self.generate_traceback()}{Error.__repr__(self)}"

    def generate_traceback(self) -> str:
        result = ""
        pos = self.pos_start
        ctx = self.context
        while ctx:
            result = (
                f"  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n"
                + result
            )
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        return "Traceback (most recent call last):\n" + result
