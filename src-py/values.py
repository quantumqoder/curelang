from types import NotImplementedType
from typing import Optional, Self, Tuple, Union

from position import Position


class Value:
    def __init__(self, value: Union[float, str, Tuple]) -> None:
        self.value: Union[float, str, Tuple] = value
        self.set_pos()

    def set_pos(
        self, start_pos: Optional[Position] = None, end_pos: Optional[Position] = None
    ) -> Self:
        self.start_pos: Optional[Position] = start_pos
        self.end_pos: Optional[Position] = end_pos
        return self

    def __repr__(self) -> str:
        return f"{self.value}"

    def __add__(self, __other: Self) -> Union[Self, NotImplementedType]:
        match __other:
            case self.__class__():
                return self.__class__(self.value + __other.value)
            case String():
                if __other.value.isdigit():
                    return Number(self.value + float(__other.value))
                return String(f"{self.value}{__other.value}")
            case Number():
                return String(f"{self.value}{__other.value}")
            case Block():
                return Block((self.value, *__other.value))
            case _:
                return NotImplemented


class Number(Value):
    def __sub__(
        self, __other: Union[Self, "String"]
    ) -> Union[Self, NotImplementedType]:
        match __other:
            case Number():
                return Number(self.value - __other.value)
            case String():
                if __other.value.isdigit():
                    return Number(self.value - float(__other.value))
        return NotImplemented

    def __mul__(self, __other: Self) -> Self:
        if isinstance(__other, Number):
            return Number(self.value * __other.value)
        return NotImplemented

    def __truediv__(self, __other: Self) -> Self:
        if isinstance(__other, Number):
            if __other.value == 0:
                return Block((__other.value,))
            return Number(self.value / __other.value)
        return NotImplemented


class String(Value):
    def __sub__(self, __other: Union[Self, Number]) -> Union[Self, NotImplementedType]:
        if isinstance(__other, String):
            return String(self.value.replace(__other.value, ""))
        return NotImplemented


class Block(Value):
    def __init__(self, value: Tuple) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"{self.value}"
