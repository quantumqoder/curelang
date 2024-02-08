from abc import abstractmethod
from typing import Optional, Self, overload

from nodes import Node
from values import Number

class Result:
    def __init__(self) -> None: ...
    @overload
    @abstractmethod
    def register(self, res: Self) -> Optional[Number]: ...
    @overload
    @abstractmethod
    def register(self, res: Self) -> Node: ...
    @overload
    @abstractmethod
    def register(self, res: Node) -> Node: ...
    