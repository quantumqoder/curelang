from abc import abstractproperty
from types import NotImplementedType
from typing import Any, Dict, List, Optional, Self, Union, override

from position import Position


class CallableSequence:
    def __init__(
        self, name: str, arguments: List[Dict[str, Any]], body: List[Self]
    ) -> None:
        self.name: str = name
        self.arguments: List[Dict[str, Any]] = arguments
        self.body: List[Self] = body
        self.value: Optional[Self] = None
        self.base: Optional[Self] = None
        self.child: Optional[Self] = None
        self.set_pos()

    def set_pos(
        self, pos_start: Optional[Position] = None, pos_end: Optional[Position] = None
    ) -> Self:
        self.pos_start: Optional[Position] = pos_start
        self.pos_end: Optional[Position] = pos_end
        return self

    def __add__(self, other: Self) -> Union[Self, NotImplementedType]:
        if isinstance(other, CallableSequence):
            return CallableSequence(
                self.name, self.arguments + other.arguments, self.body + other.body
            )
        return NotImplemented

    @property
    def isdigit(self) -> bool:
        match self.value:
            case int() | float():
                return True
            case str():
                return self.value.isdigit()
            case _:
                return False

    @property
    def length(self) -> int:
        if self.value and isinstance(self.value, str):
            return len(self.value)
        if self.body:
            return len(self.body)

    @abstractproperty
    def labels(self) -> NotImplementedType: ...

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.value

    def __repr__(self) -> str:
        return f"{self.name}({self.arguments})"


class Number(CallableSequence):
    @override
    def __init__(self, value: float) -> None:
        super().__init__("Number", [], [])
        self.value: float = value
        self.set_pos()

    @override
    @property
    def labels(self) -> List:
        return []

    def __neg__(self) -> Self:
        return Number(-self.value)

    @override
    def __add__(self, other: Self) -> Self:
        return Number(self.value + other.value)

    @override
    def __sub__(self, other: Self) -> Self:
        return Number(self.value - other.value)

    @override
    def __mul__(self, other: Self) -> Self:
        return Number(self.value * other.value)

    @override
    def __truediv__(self, other: Self) -> Self:
        return Number(self.value / other.value)

    @override
    def __call__(self) -> Self:
        return self

    @override
    def __repr__(self) -> str:
        return f"{self.value}"


# class Value:
#     def __init__(self, value: Union[float, str, Tuple]) -> None:
#         self.value: Union[float, str, Tuple] = value
#         self.set_pos()

#     def set_pos(
#         self, start_pos: Optional[Position] = None, end_pos: Optional[Position] = None
#     ) -> Self:
#         self.start_pos: Optional[Position] = start_pos
#         self.end_pos: Optional[Position] = end_pos
#         return self

#     def __repr__(self) -> str:
#         return f"{self.value}"

#     def __add__(self, __other: Self) -> Union[Self, NotImplementedType]:
#         match __other:
#             case self.__class__():
#                 return self.__class__(self.value + __other.value)
#             case String():
#                 if __other.value.isdigit():
#                     return Number(self.value + float(__other.value))
#                 return String(f"{self.value}{__other.value}")
#             case Number():
#                 return String(f"{self.value}{__other.value}")
#             case Block():
#                 return Block((self.value, *__other.value))
#             case _:
#                 return NotImplemented


# class Number(Value):
#     def __sub__(
#         self, __other: Union[Self, "String"]
#     ) -> Union[Self, NotImplementedType]:
#         match __other:
#             case Number():
#                 return Number(self.value - __other.value)
#             case String():
#                 if __other.value.isdigit():
#                     return Number(self.value - float(__other.value))
#         return NotImplemented

#     def __mul__(self, __other: Self) -> Self:
#         if isinstance(__other, Number):
#             return Number(self.value * __other.value)
#         return NotImplemented

#     def __truediv__(self, __other: Self) -> Self:
#         if isinstance(__other, Number):
#             if __other.value == 0:
#                 return Block((__other.value,))
#             return Number(self.value / __other.value)
#         return NotImplemented


# class String(Value):
#     def __sub__(self, __other: Union[Self, Number]) -> Union[Self, NotImplementedType]:
#         if isinstance(__other, String):
#             return String(self.value.replace(__other.value, ""))
#         return NotImplemented


# class Block(Value):
#     def __init__(self, value: Tuple) -> None:
#         self.value = value

#     def __repr__(self) -> str:
#         return f"{self.value}"
