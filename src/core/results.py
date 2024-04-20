from typing import Optional, Self, Union, overload

from errors import Error
from nodes import Node
from tokens import Token
from values import Number


class Result:
    def __init__(self) -> None:
        self.error: Optional[Error] = None
        self.value: Optional[Union[Node, Number]] = None

    def register(self, res: Union[Self, Token, Number]) -> Union[Node, Number]:
        if isinstance(res, Result):
            if res.error:
                self.error = res.error
            return res.value
        return res

    def success(self, value: Union[Node, Number]) -> Self:
        self.value = value
        return self

    def failure(self, error: Error) -> Self:
        self.error = error
        return self

    def __str__(self) -> str:
        return f"{self.value}"

    def __repr__(self) -> str:
        return f"Result({self.error=}, {self.value=})"

    def __bool__(self) -> bool:
        return self.error is None

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Result):
            return NotImplemented
        return self.error == other.error and self.value == other.value
