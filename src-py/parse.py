import logging
from enum import auto
from typing import Callable, List, Optional, Self

from errors import InvalidSyntaxError
from nodes import BinOpNode, Node, NumberNode, UnaryOpNode
from results import ParseResult
from tokens import TOKEN_TYPE, Token

logger = logging.getLogger("cse.parser")


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        logger.debug("initiate parser")
        self.tokens: List[Token] = tokens
        self.tok_idx: int = -1
        self.advance()

    def advance(self) -> Token:
        self.current_token: Optional[Token] = None
        if self.tok_idx < len(self.tokens) - 1:
            self.tok_idx += 1
            self.current_token = self.tokens[self.tok_idx]
        logger.debug("advance parser", extra={"cur_token_idx": self.tok_idx})
        return self.current_token

    def parse(self) -> ParseResult:
        logger.info("parsing tokens")
        res: ParseResult = self.expr()
        if res.error and self.current_token.type != TOKEN_TYPE.EOF:
            return res.failure(
                InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected '+', '-', '*' or '/'",
                )
            )
        logger.debug("parse result", extra={"result": res.node})
        return res.success(res.node)

    def expr(self) -> ParseResult:
        logger.debug("evaluate expression")
        return self.bin_op(self.term, [TOKEN_TYPE.PLUS, TOKEN_TYPE.MINUS])

    def term(self) -> ParseResult:
        logger.debug("evaluate term")
        return self.bin_op(self.factor, [TOKEN_TYPE.MUL, TOKEN_TYPE.DIV])

    def factor(self) -> ParseResult:
        logger.debug("evaluate factor")
        res = ParseResult()
        token: Token = self.current_token
        match token.type:
            case TOKEN_TYPE.PLUS | TOKEN_TYPE.MINUS:
                res.register(self.advance())
                factor = res.register(self.factor())
                if res.error:
                    return res
                return res.success(UnaryOpNode(token, factor))
            case TOKEN_TYPE.NUMBER:
                res.register(self.advance())
                return res.success(NumberNode(token))
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

    def bin_op(
        self, func: Callable[[Self], ParseResult], ops: List[auto]
    ) -> ParseResult:
        logger.debug("binary operation", extra={"call": func.__name__, "ops": ops})
        res = ParseResult()
        left_node: Node = res.register(func())
        if res.error:
            return res
        while self.current_token.type in ops:
            op_tok: Token = self.current_token
            res.register(self.advance())
            right_node: Node = res.register(func())
            if res.error:
                return res
            left_node = BinOpNode(left_node, op_tok, right_node)
        return res.success(left_node)