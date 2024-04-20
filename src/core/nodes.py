from abc import abstractmethod
from dataclasses import dataclass
from typing import Self, Union

from core.tokens import Token
from utils.log_utils import get_logger

logger = get_logger("cure.parser")


class Node:
    def __init__(self) -> None:
        logger.debug(f"{self}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"

    @abstractmethod
    def __str__(self) -> str:
        pass


@dataclass
class NumberNode:
    num_token: Token

    def __post_init__(self) -> Self:
        self.pos_start = self.num_token.pos_start
        self.pos_end = self.num_token.pos_end


@dataclass
class UnaryOpNode:
    op_token: Token
    node: NumberNode

    def __post_init__(self) -> Self:
        self.pos_start = self.op_token.pos_start
        self.pos_end = self.node.pos_end


@dataclass
class BinOpNode:
    left_node: NumberNode
    op_token: Token
    right_node: NumberNode

    def __post_init__(self) -> Self:
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end


@dataclass
class VarAccessNode:
    var_token: Token

    def __post_init__(self) -> Self:
        self.pos_start = self.var_token.pos_start
        self.pos_end = self.var_token.pos_end


@dataclass
class VarAssignNode:
    var_token: Token
    val_node: Union[NumberNode, UnaryOpNode, BinOpNode]

    def __post_init__(self) -> Self:
        self.pos_start = self.var_token.pos_start
        self.pos_end = self.val_node.pos_end
