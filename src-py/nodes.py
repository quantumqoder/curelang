import logging
from abc import abstractmethod
from typing import override

from position import Position
from tokens import Token

logger = logging.getLogger("cse.parser")


class Node:
    def __init__(self) -> None:
        logger.debug(f"{self}")

    @abstractmethod
    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.__repr__()})"


class NumberNode(Node):
    @override
    def __init__(self, token: Token) -> None:
        self.token: Token = token
        self.pos_start: Position = token.pos_start
        self.pos_end: Position = token.pos_end
        super().__init__()

    @override
    def __repr__(self) -> str:
        return f"{self.token}"


class UnaryOpNode(Node):
    @override
    def __init__(self, token: Token, node: NumberNode) -> None:
        self.token: Token = token
        self.node: NumberNode = node
        self.pos_start: Position = token.pos_start
        self.pos_end: Position = node.pos_end
        super().__init__()

    @override
    def __repr__(self) -> str:
        return f"{self.token}, {self.node}"


class BinOpNode(Node):
    @override
    def __init__(
        self, left_node: NumberNode, token: Token, right_node: NumberNode
    ) -> None:
        self.left_node: NumberNode = left_node
        self.token: Token = token
        self.right_node: NumberNode = right_node
        self.pos_start: Position = left_node.pos_start
        self.pos_end: Position = right_node.pos_end
        super().__init__()

    @override
    def __repr__(self) -> str:
        return f"{self.left_node}, {self.token}, {self.right_node}"
