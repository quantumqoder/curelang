import logging
from enum import auto
from typing import Callable, List, Optional, Self

from errors import InvalidSyntaxError
from nodes import BinOpNode, Node, NumberNode, UnaryOpNode
from results import Result
from tokens import TOKEN_TYPE, Token

logger = logging.getLogger("cse.parser")


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        logger.debug("initiate parser")
        self.tokens: List[Token] = tokens
        self.tok_idx: int = -1
        self.current_token: Optional[Token] = None
        self.advance()

    def advance(self) -> Token:
        if self.tok_idx < len(self.tokens):
            self.tok_idx += 1
            self.current_token = self.tokens[self.tok_idx]
        logger.debug(
            "advance parser",
            extra={self.tok_idx: self.current_token},
        )
        return self.current_token

    def parse(self) -> Result:
        logger.info("parsing tokens")
        res: Result = self.expr()
        if res.error and self.current_token.type != TOKEN_TYPE.EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected '+', '-', '*' or '/'",
                )
            )
        logger.debug("parse result", extra={"result": res.value})
        return res.success(res.value)

    def expr(self) -> Result:
        logger.info("evaluate expression")
        return self.bin_op(self.term, [TOKEN_TYPE.PLUS, TOKEN_TYPE.MINUS])

    def term(self) -> Result:
        logger.info("evaluate term")
        return self.bin_op(self.factor, [TOKEN_TYPE.MUL, TOKEN_TYPE.DIV])

    def bin_op(self, func: Callable[[Self], Result], ops: List[auto]) -> Result:
        logger.debug("binary operation", extra={"func": func.__name__, "ops": ops})
        res = Result()
        left_node: Node = res.register(func())
        logger.debug(f"executed {func.__name__}", extra={"left node": left_node})
        if res.error:
            return res
        while self.current_token.type in ops:
            op_tok: Token = self.current_token
            logger.debug(
                "binary operation", extra={"current operation": self.current_token.type}
            )
            res.register(self.advance())
            right_node: Node = res.register(func())
            logger.debug(f"executed {func.__name__}", extra={"right node": right_node})
            if res.error:
                return res
            left_node = BinOpNode(left_node, op_tok, right_node)
            logger.debug(f"{left_node}")
        return res.success(left_node)

    def factor(self) -> Result:
        logger.info("evaluate factor")
        res = Result()
        token: Token = self.current_token
        logger.debug("in factor", extra={"current token": token})
        match token.type:
            case TOKEN_TYPE.PLUS | TOKEN_TYPE.MINUS:
                res.register(self.advance())
                factor = res.register(self.factor())
                if res.error:
                    return res
                return res.success(UnaryOpNode(token, factor))
            case TOKEN_TYPE.NUMBER:
                node = NumberNode(token)
                res.register(self.advance())
                return res.success(node)
            case TOKEN_TYPE.LEFT_BRAKET:
                res.register(self.advance())
                expr: Node = res.register(self.expr())
                if res.error:
                    return res
                if self.current_token.type != TOKEN_TYPE.RIGHT_BRAKET:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_token.pos_start,
                            self.current_token.pos_end,
                            "Expected ')'",
                        )
                    )
                res.register(self.advance())
                return res.success(expr)
        return res.failure(
            InvalidSyntaxError(token.pos_start, token.pos_end, "Expected number")
        )
