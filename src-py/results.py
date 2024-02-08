from abc import abstractmethod
from typing import Optional, Self, Union

from errors import Error
from nodes import Node
from values import Number


class Result:
    def __init__(self) -> None:
        self.error: Optional[Error] = None

    @abstractmethod
    def register(self, res: Union[Self, Node]) -> Union[Optional[Number], Node]: ...

    def success(self, *args) -> Self:
        if self.__class__ not in (ParseResult, RuntimeResult):
            raise
        attr = "node" if self.__class__ == ParseResult else "value"
        setattr(self, attr, args[0])
        return self

    def failure(self, error: Error) -> Self:
        self.error = error
        return self


class ParseResult(Result):
    def __init__(self) -> None:
        Result.__init__(self)
        self.node: Optional[Node] = None

    def register(self, res: Union[Self, Node]) -> Node:
        if not isinstance(res, ParseResult):
            return res
        if res.error:
            self.error = res.error
        return res

    def __repr__(self) -> str:
        return f"ParseResult({self.error=}, {self.node=})"

    def __bool__(self) -> bool:
        return self.error is None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ParseResult):
            return NotImplemented
        return self.error == other.error and self.node == other.node


class RuntimeResult(Result):
    def __init__(self) -> None:
        Result.__init__(self)
        self.value: Optional[Number] = None

    def register(self, res: Self) -> Optional[Number]:
        if res.error:
            self.error = res.error
        return res.value
