# Getting Started

CURE (Callable Units Recursive Evaluator) is a programming language designed for developers who prefer a **concise and intuitive syntax** based on typographical symbols. This guide will introduce you to the core concepts of CURE and equip you to begin writing your own CURE programs.

**Prerequisites:**

* Familiarity with basic programming concepts (variables, functions, etc.) is helpful but not essential.
* A text editor or IDE capable of working with plain text files.

**Hello, CURE!**

Your first CURE program will be a classic: printing "Hello, World!". Here's how it looks in CURE:

```cure
$ #!/cure
dump("Hello, World!")
```

**Explanation:**

* `#!/cure`: This line is optional and specifies that the code should be interpreted by the CURE interpreter.
* `dump("Hello, World!")`: This is the core function call in CURE.
  * `dump`: This is a built-in function that outputs the provided string to the console.
  * `"Hello, World!"`: The string literal to be printed.

**Running the Program:**

1. Save the code in a file named `hello.cure` (or any filename with the `.cure` extension).
2. Open a terminal window and navigate to the directory where you saved the file.
3. Run the program using:

```bash
cure ./hello.cure
```

You should see "Hello, World!" printed on the console.

You can also compile the file to an executable using:

```bash
cure -c ./hello.cure
```

And, then run the file:

```bash
./hello
```

**CURE Fundamentals:**

* **Functions:** As you saw, everything in CURE revolves around functions. Functions are defined using a single, modular structure that incorporates input processing, logic, and output generation.
* **Typographical Symbols:** CURE relies on a set of typographical symbols to construct code. The specific symbols and their combinations determine the program's behavior.

**Beyond Hello World:**

This is just a starting point! CURE offers various functionalities for building more complex programs. Continue for more exiting features to come.

**Remember:** CURE is designed to be user-centric and extensible. Don't hesitate to experiment and explore its capabilities to create innovative programs!
