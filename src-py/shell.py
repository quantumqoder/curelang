import atexit
import json
import logging
import logging.config
import pathlib

import cse

logger = logging.getLogger("cse")
config_file = pathlib.Path(".//src-py//log_config.json")
with open(config_file) as f:
    config = json.load(f)
logging.config.dictConfig(config)
queue_handler = logging.getHandlerByName("queue_handler")
if queue_handler:
    queue_handler.listener.start()
    atexit.register(queue_handler.listener.stop)
logger.info("initial logger setup")

if __name__ == "__main__":
    while True:
        text: str = input("cse> ")
        result, error = cse.execute("<stdin>", text)
        if error:
            print(error)
        else:
            print(result)
