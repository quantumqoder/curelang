import logging
from functools import partial
from typing import List, Optional, Tuple, Union

from errors import InvalidCharError
from core.position import Position
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
    ) -> Union[
        Tuple[List[Token], None],
        Tuple[List, InvalidCharError],
    ]:
        logger.info("generating tokens")
        tokens: List[Token] = []
        while self.cur_char != None:
            match self.cur_char:
                case " " | "\t":
                    self.advance()
                    continue
                case self.cur_char if self.cur_char.isdigit():
                    token = self.make_number()
                    tokens.append(token)
                    continue
                case self.cur_char if self.cur_char.isalpha():
                    token = self.make_identifier()
                    tokens.append(token)
                    continue
                case "=":
                    token = Token(TOKEN_TYPE.EQUAL, pos_start=self.cur_pos)
                case "+":
                    token = Token(TOKEN_TYPE.PLUS, pos_start=self.cur_pos)
                case "-":
                    token = Token(TOKEN_TYPE.HYPHEN, pos_start=self.cur_pos)
                case "*":
                    token = Token(TOKEN_TYPE.STAR, pos_start=self.cur_pos)
                case "/":
                    token = Token(TOKEN_TYPE.SLASH, pos_start=self.cur_pos)
                case "^":
                    token = Token(TOKEN_TYPE.POWER, pos_start=self.cur_pos)
                case "(":
                    token = Token(TOKEN_TYPE.LPAREN, pos_start=self.cur_pos)
                case ")":
                    token = Token(TOKEN_TYPE.RPAREN, pos_start=self.cur_pos)
                case _:
                    pos_start: Position = self.cur_pos.copy()
                    cur_char: str = self.cur_char
                    self.advance()
                    return [], InvalidCharError(
                        pos_start, self.cur_pos, f"'{cur_char}'"
                    )
            tokens.append(token)
            self.advance()
        tokens.append(Token(TOKEN_TYPE.EOF, pos_start=self.cur_pos))
        logger.debug(f"{tokens=}")
        return tokens, None

    def make_number(self) -> Token:
        number: str = ""
        dot_count: int = 0
        pos_start: Position = self.cur_pos.copy()
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
        return Token(TOKEN_TYPE.NUMBER, float(number), pos_start, self.cur_pos)

    def make_identifier(self) -> Token:
        identifier: str = ""
        pos_start: Position = self.cur_pos.copy()
        while self.cur_char != None and (
            self.cur_char.isalpha() or self.cur_char.isdigit() or self.cur_char == "_"
        ):
            identifier += self.cur_char
            self.advance()
        cur_pos: Position = self.cur_pos.copy()
        # and then move ahead to check if the next character is =, then identifier is identifier else its a type
        return Token(TOKEN_TYPE.IDENTIFIER, identifier, pos_start, self.cur_pos)


if __name__ == "__main__":
    par_lexer = partial(Lexer, "<module>")
    while True:
        ftext = input("cse> ")
        lexer = par_lexer(ftext)
        tokens, error = lexer.make_tokens()
        print(error if error else tokens)
