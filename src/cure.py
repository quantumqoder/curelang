import rich

from core.context import Context
from core.interpreter import Interpreter
from core.lexer import Lexer
from core.parse import Parser
from core.symbol_table import SymbolTable
from core.values import Number
from utils.log_utils import get_logger

logger = get_logger("cure")

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number(0))


def execute(fn: str, text: str):
    logger.info("Executing %s", fn)

    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    logger.debug("generated tokens", extra={"tokens": tokens})
    rich.print(f"{tokens=}")
    if error:
        logger.error(error)
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    logger.debug("final node", extra={"node": ast.value})
    rich.print(f"{ast.value=}")
    if ast.error:
        logger.error(ast.error)
        return None, ast.error

    # Execute program
    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.value, context)
    logger.debug("", extra={"symbol_table": context.symbol_table})
    return result, None


if __name__ == "__main__":
    import sys

    fn = sys.argv[1]
    with open(fn, "r") as f:
        text = f.read()
    result, error = execute(fn, text)
    print(result if error is None else error)
