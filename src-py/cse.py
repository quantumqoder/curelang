import logging

from interpreter import Interpreter
from lexer import Lexer
from parse import Parser

logger = logging.getLogger("cse")


def execute(fn: str, text: str):
    logger.info("Executing %s", fn)

    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    logger.debug("generated tokens", extra={"tokens": tokens})
    print(f"{tokens=}")
    if error:
        logger.error(error)
        return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    logger.debug("final node", extra={"node": ast.node})
    print(f"{ast.node=}")
    if ast.error:
        logger.error(ast.error)
        return None, ast.error

    # Execute program
    interpreter = Interpreter()
    result = interpreter.visit(ast.node)
    return result, None
