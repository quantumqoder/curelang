import logging
from typing import Callable, NoReturn, Union

from core.context import Context
from nodes import BinOpNode, Node, NumberNode, UnaryOpNode
from results import Result
from tokens import TOKEN_TYPE
from values import Number

logger = logging.getLogger("cse")


class Interpreter:
    def visit(self, node: Node, context: Context) -> Union[Result, NoReturn]:
        method_name: str = f"visit_{type(node).__name__.lower()}"
        logger.info(f"{method_name}")
        method: Callable[[Node], Union[Number, NoReturn]] = getattr(
            self,
            method_name,
            self.no_visit_method,
        )
        return method(node, context)

    def no_visit_method(self, node: Node, _: Context) -> NoReturn:
        raise Exception(f"No visit_{type(node).__name__.lower()} method defined")

    def visit_varaccessnode(self, node: Node, context: Context) -> Result:
        logger.debug("var access node")
        res = Result()
        var_name: str = node.token.value
        var_value: Number = context.symbol_table.get(var_name)
        if not var_value:
            return res.failure(
                f"'{var_name}' is not defined",
            )
        return res.success(var_value.set_pos(node.pos_start, node.pos_end))

    def visit_varassignnode(self, node: Node, context: Context) -> Result:
        logger.debug("var assign node")
        res = Result()
        var_name: str = node.token.value
        var_value: Number = res.register(self.visit(node.node, context))
        if res.error:
            return res
        context.symbol_table.set(var_name, var_value)
        return res.success(var_value)

    def visit_numbernode(self, node: NumberNode, context: Context) -> Result:
        return Result().success(
            Number(node.token.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    def visit_binopnode(self, node: BinOpNode, context: Context) -> Result:
        logger.debug("binary op node")
        res = Result()
        left_node: Number = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right_node: Number = res.register(self.visit(node.right_node, context))
        if res.error:
            return res
        # error = None
        match node.token.type:
            case TOKEN_TYPE.PLUS:
                result, error = (left_node + right_node), None
            case TOKEN_TYPE.MINUS:
                result, error = (left_node - right_node), None
            case TOKEN_TYPE.MULTIPLY:
                result, error = (left_node * right_node), None
            case TOKEN_TYPE.DIVIDE:
                result, error = (left_node / right_node), None
            case TOKEN_TYPE.POWER:
                result, error = (left_node**right_node), None
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
        if error:
            return res.failure(error)
        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_unaryopnode(self, node: UnaryOpNode, context: Context) -> Result:
        logger.debug("unary op node")
        res = Result()
        number: Number = res.register(self.visit(node.node, context))
        if res.error:
            return res
        error = None
        match node.token.type:
            case TOKEN_TYPE.PLUS:
                result, error = number, None
            case TOKEN_TYPE.MINUS:
                result, error = -number, None
            case _:
                raise Exception(f"Unknown unary operator {node.token.type}")
        if error:
            return res.failure(error)
        return res.success(result.set_pos(node.pos_start, node.pos_end))
