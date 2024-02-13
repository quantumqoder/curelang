import logging

from position import Position
from tokens import Token

logger = logging.getLogger("cse.parser")


class Node:
    def __init__(self, token: Token) -> None:
        self.pos_start: Position = token.pos_start
        self.token: Token = token
        self.pos_end: Position = token.pos_end
        logger.debug(f"{__class__.__name__}", extra={"node": __class__.__str__(self)})

    def __str__(self) -> str:
        return f"{self.token}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"


class NumberNode(Node): ...


class UnaryOpNode(Node):
    def __init__(self, token: Token, node: Node) -> None:
        Node.__init__(self, token)
        self.node: Node = node
        self.pos_end = node.pos_end
        logger.debug(f"{__class__.__name__}", extra={"node": __class__.__str__(self)})

    def __str__(self) -> str:
        return f"{Node.__str__(self)}, {self.node}"


class BinOpNode(Node):
    def __init__(self, left_node: Node, token: Token, right_node: Node) -> None:
        UnaryOpNode.__init__(self, token, right_node)
        self.left_node: Node = left_node
        self.right_node: Node = right_node
        self.pos_start = left_node.pos_start
        logger.debug(f"{__class__.__name__}", extra={"node": __class__.__str__(self)})

    def __str__(self) -> str:
        return f"{self.left_node}, {UnaryOpNode.__str__(self)}"
