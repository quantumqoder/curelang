import cure

if __name__ == "__main__":
    while True:
        text: str = input("cure> ")
        result, error = cure.execute("<stdin>", text)
        print(result if error is None else error)
