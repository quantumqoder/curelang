from typing import Any, Dict, Optional, Self


class SymbolTable:
    def __init__(self) -> None:
        self.symbols: Dict[str, Any] = {}
        self.parent: Optional[Self] = None

    def get(self, name: str) -> Optional[str]:
        value = self.symbols.get(name, None) # May need to replace with setdefault for the implementation logic of all the symbols available at all times
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name: str, value: Any) -> None:
        self.symbols[name] = value

    def remove(self, name: str) -> None:
        del self.symbols[name]
