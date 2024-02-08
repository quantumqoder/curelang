from enum import auto
from typing import overload

from position import Position

class Token:
    @overload
    def __init__(self, tok_type: auto) -> None: ...
    @overload
    def __init__(
        self, tok_type: auto, tok_val: float, start_pos: Position, end_pos: Position
    ) -> None: ...
    def __repr__(self) -> str: ...
