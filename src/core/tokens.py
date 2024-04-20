from enum import Enum, auto
from typing import Optional, Self

from core.position import Position


class TOKEN_TYPE(Enum):
    NUMBER = auto() # 0-9
    IDENTIFIER = auto() # A-Za-z0-9_
    EQUAL = auto() # =
    PLUS = auto() # +
    HYPHEN = auto() # -
    STAR = auto() # *
    SLASH = auto() # /
    POWER = auto() # ^
    MODULUS = auto() # %
    LESS_THAN = auto() # <
    GREATER_THAN = auto() # >
    NOT = auto() # ~
    AND = auto() # &
    OR = auto() # |
    QUERY = auto() # ?
    COLON = auto() # :
    COMMA = auto() # ,
    LBRACE = auto() # {
    RBRACE = auto() # }
    LPAREN = auto() # (
    RPAREN = auto() # )
    QUOTES = auto() # "
    LBRAKET = auto() # [
    RBRAKET = auto() # ]
    HASH = auto() # #
    AT = auto() # @
    DOT = auto() # .

class Token:
    def __init__(
        self,
        tok_type: auto,
        tok_val: Optional[float]=None,
        pos_start: Optional[Position]=None,
        pos_end: Optional[Position]=None,
    ) -> None:
        self.type: auto = tok_type
        self.value: Optional[float] = tok_val
        self.pos_start = None
        self.pos_end = None
        if pos_start:
            self.pos_start: Position = pos_start.copy()
            self.pos_end: Position = pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            self.pos_end = pos_end.copy()

    def __repr__(self) -> str:
        return f"<{self.type}{f": {self.value}" if self.value else ""}>"

    def __bool__(self, other: Self) -> bool:
        return self.type == other.type and self.value == other.value

    def copy(self) -> Self:
        return Token(self.type, self.value, self.pos_start, self.pos_end)
