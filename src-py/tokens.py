from enum import Enum, auto
from typing import Optional

from position import Position


class TOKEN_TYPE(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    LBRAKET = auto()
    RBRAKET = auto()
    EOF = auto()


class Token:
    def __init__(self, tok_type: auto, tok_val: Optional[float] = None, start_pos: Optional[Position] = None, end_pos: Optional[Position] = None) -> None:
        self.type: auto = tok_type
        self.value: Optional[float] = tok_val
        self.pos_start = None
        self.pos_end = None
        if start_pos:
            self.pos_start: Position = start_pos.copy()
            self.pos_end: Position = start_pos.copy()
            self.pos_end.advance()
        if end_pos:
            self.pos_end = end_pos.copy()

    def __repr__(self) -> str:
        return f"{self.type}{f": {self.value}" if self.value else ""}"
