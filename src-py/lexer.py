import logging
from tracemalloc import start
from typing import List, Optional, Tuple, Union

from errors import InvalidCharError
from position import Position
from tokens import TOKEN_TYPE, Token

logger = logging.getLogger("cse.lexer")


class Lexer:
    def __init__(self, fn: str, text: str) -> None:
        logger.debug("initiate lexer")
        self.fn: str = fn
        self.text: str = text
        self.cur_pos: Position = Position(-1, 0, -1, fn, text)
        self.cur_char: Optional[str] = None
        self.advance()

    def advance(self) -> None:
        self.cur_pos.advance(self.cur_char)
        self.cur_char = (
            self.text[self.cur_pos.index]
            if self.cur_pos.index < len(self.text)
            else None
        )
        logger.debug("advance lexer", extra={"self.cur_char": self.cur_char})

    def make_tokens(
        self,
    ) -> Union[Tuple[List[Token], None], Tuple[List, InvalidCharError]]:
        logger.info("generating tokens")
        tokens: List[Token] = []
        while self.cur_char != None:
            match self.cur_char:
                case " " | "\t":
                    self.advance()
                    continue
                case self.cur_char if self.cur_char.isdigit():
                    token = self.make_number()
                case "+":
                    token = Token(TOKEN_TYPE.PLUS, start_pos=self.cur_pos)
                case "-":
                    token = Token(TOKEN_TYPE.MINUS, start_pos=self.cur_pos)
                case "*":
                    token = Token(TOKEN_TYPE.MUL, start_pos=self.cur_pos)
                case "/":
                    token = Token(TOKEN_TYPE.DIV, start_pos=self.cur_pos)
                case "^":
                    token = Token(TOKEN_TYPE.POW, start_pos=self.cur_pos)
                case "(":
                    token = Token(TOKEN_TYPE.LEFT_BRAKET, start_pos=self.cur_pos)
                case ")":
                    token = Token(TOKEN_TYPE.RIGHT_BRAKET, start_pos=self.cur_pos)
                case _:
                    pos_start: Position = self.cur_pos.copy()
                    cur_char: str = self.cur_char
                    self.advance()
                    return [], InvalidCharError(
                        pos_start, self.cur_pos, f"'{cur_char}'"
                    )
            tokens.append(token)
            self.advance()
        tokens.append(Token(TOKEN_TYPE.EOF, start_pos=self.cur_pos))
        logger.debug(f"{tokens=}")
        return tokens, None

    def make_number(self) -> Token:
        number: str = ""
        dot_count: int = 0
        start_pos: Position = self.cur_pos.copy()
        while self.cur_char != None and (
            self.cur_char.isdigit() or self.cur_char == "."
        ):
            if self.cur_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                number += "."
                self.advance()
                continue
            number += self.cur_char
            self.advance()
        logger.debug(f"{number=}")
        return Token(TOKEN_TYPE.NUMBER, float(number), start_pos, self.cur_pos)
