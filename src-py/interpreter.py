from typing import Callable, NoReturn, Union

from nodes import BinOpNode, Node, NumberNode, UnaryOpNode
from results import RuntimeResult
from tokens import TOKEN_TYPE
from values import Number


class Interpreter:
    def visit(self, node: Node) -> Union[Number, NoReturn]:
        method_name: str = f"visit_{type(node).__name__.lower()}"
        method: Callable[[Node], Union[Number, NoReturn]] = getattr(
            self, method_name, self.no_visit_method
        )
        return method(node)

    def no_visit_method(self, node: Node) -> NoReturn:
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_numbernode(self, node: NumberNode) -> RuntimeResult:
        return RuntimeResult().success(
            Number(node.token.value).set_pos(node.pos_start, node.pos_end)
        )

    def visit_binopnode(self, node: BinOpNode) -> Number:
        res = RuntimeResult()
        left_node = res.register(self.visit(node.left_node))
        if res.error:
            return res
        right_node = res.register(self.visit(node.right_node))
        if res.error:
            return res
        # error = None
        match node.token.type:
            case TOKEN_TYPE.PLUS:
                result = left_node + right_node
            case TOKEN_TYPE.MINUS:
                result = left_node - right_node
            case TOKEN_TYPE.MUL:
                result = left_node * right_node
            case TOKEN_TYPE.DIV:
                result = left_node / right_node
            case TOKEN_TYPE.POW:
                pass
            case TOKEN_TYPE.EQ:
                pass
            case TOKEN_TYPE.NE:
                pass
            case TOKEN_TYPE.LT:
                pass
            case TOKEN_TYPE.GT:
                pass
            case TOKEN_TYPE.LE:
                pass
            case TOKEN_TYPE.GE:
                pass
            case _:
                raise Exception(f"Unknown binary operator {node.token.type}")
        return result.set_pos(node.pos_start, node.pos_end)

    def visit_unaryopnode(self, node: UnaryOpNode) -> Number:
        number = self.visit(node.node)
        match node.token.type:
            case TOKEN_TYPE.PLUS:
                result = number
            case TOKEN_TYPE.MINUS:
                result = -number
            case _:
                raise Exception(f"Unknown unary operator {node.token.type}")
        return result.set_pos(node.pos_start, node.pos_end)
