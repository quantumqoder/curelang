from dataclasses import dataclass
from typing import Optional, Self

from core.position import Position
from core.symbol_table import SymbolTable


@dataclass
class Context:
    display_name: str
    parent: Optional[Self] = None
    parent_entry_pos: Optional[Position] = None
    symbol_table: Optional[SymbolTable] = None
