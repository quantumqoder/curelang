from typing import List, Optional, Self

from tokens import Token, TOKEN_TYPE
from values import Number


def execute(fn: str, ftext: str) -> None:
    evaluator = Evaluator(fn, ftext)
    evaluator.execute()


class Evaluator:
    def __init__(self, fn: str, ftext: str, index: int = -1, line_num: int = 0, column_num: int = -1) -> None:
        self.fn: str = fn
        self.ftext: str = ftext
        self.index: int = index
        self.line_num: int = line_num
        self.column_num: int = column_num
        self.cur_char: Optional[str] = None
        self.advance()

    def copy(self) -> Self:
        other = Evaluator(self.fn, self.ftext)
        other.index = self.index
        other.line_num = self.line_num
        other.column_num = self.column_num
        return other

    def advance(self, cur_char: Optional[str] = None) -> Self:
        self.index += 1
        if self.index < len(self.ftext):
            self.cur_char = self.ftext[self.index]
        else:
            self.cur_char = None
        self.column_num += 1
        if cur_char == "\n":
            self.line_num += 1
            self.column_num = 0
        return self

    def execute(self) -> Number:
        self.make_tokens()
        self.parse()
        return self.visit()

    def make_tokens(self) -> None:
        self.tokens: List[Token] = []
        while self.cur_char != None:
            match self.cur_char:
                case " " | "\t":
                    self.advance()
                    continue
                case self.cur_char if self.cur_char.isdigit():
                    self.tokens.append(self.make_number())
                    continue
                case "+":
                    self.tokens.append(Token(TOKEN_TYPE.PLUS, start_pos=self.cur_pos))
                case "-":
                    self.tokens.append(Token(TOKEN_TYPE.MINUS, start_pos=self.cur_pos))
                case "*":
                    self.tokens.append(Token(TOKEN_TYPE.MUL, start_pos=self.cur_pos))
                case "/":
                    self.tokens.append(Token(TOKEN_TYPE.DIV, start_pos=self.cur_pos))
                case "^":
                    self.tokens.append(Token(TOKEN_TYPE.POW, start_pos=self.cur_pos))
                case "(":
                    self.tokens.append(Token(TOKEN_TYPE.LEFT_BRAKET, start_pos=self.cur_pos))
                case ")":
                    self.tokens.append(Token(TOKEN_TYPE.RIGHT_BRAKET, start_pos=self.cur_pos))
                case _:
                    return
        return

    def parse(self) -> None:
        self.tok_index = -1
        self.current_token: Optional[Token] = None

        def advance(self) -> Token:
            if self.tok_index < len(self.tokens):
                self.tok_idx += 1
                self.current_token =

    def visit(self) -> Union[Number, NoReturn]:
        method_name: str = f"visit_{type(self.node).__name__.lower()}"
        logger.info(f"{method_name}")
        method: Callable[[Node], Union[Number, NoReturn]] = getattr(
            self, method_name, self.no_visit_method
        )
        return method(self.node)

    def no_visit_method(self, node: Node) -> NoReturn:
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_numbernode(self, node: NumberNode) -> Result:
        return Result().success(
            Number(node.token.value).set_pos(node.pos_start, node.pos_end)
        )

    def visit_binopnode(self, node: BinOpNode) -> Number:
        logger.debug("binary op node")
        res = Result()
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
                result = left_node**right_node
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
