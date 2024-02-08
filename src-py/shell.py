import cse
from log_utils import logger

logger.info("initial logger setup")

if __name__ == "__main__":
    while True:
        text: str = input("cse> ")
        result, error = cse.execute("<stdin>", text)
        if error:
            print(error)
        else:
            print(result)
