import atexit
import json
import logging
import logging.config
import pathlib

import rich

from core.context import Context
from interpreter import Interpreter
from lexer import Lexer
from parse import Parser
from symbol_table import SymbolTable
from values import Number

logger = logging.getLogger("cse")

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
    return result, None


if __name__ == "__main__":
    import sys

    config_file = pathlib.Path(".//src//log_config.json")
    with open(config_file) as f:
        config = json.load(f)
    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)
    logger.info("initial logger setup")

    fn = sys.argv[1]
    with open(fn, "r") as f:
        text = f.read()
    result, error = execute(fn, text)
    print(result if error is None else error)
