```
Foo <- {
    a,
    1,
    () <- {
        a <- 5
    },
    foo(b) <- {
        b <-^ 2,
        a + b
    },
    lambda(x) <- a^a
}
```

Everything is a set; modules, classes, functions, everything and anything with multiple lines (basically, a code block) is a set. Since, sets have elements, thus single-line codes are elements, and since single-line codes are elements, they can also be assigned to a variable (or a lambda function if they're defined with parenthesis). Assignment itself is an element, and thus sets can contain assignment.

Now, since everything is a set, thus all algebraic operations on a set are applicable.

1. Sets can be added together (`+`). This is equivalent to a set union. Since, classes are also set, inheritance can be implemented by just adding a code block to the class definition.
    ```
    Foo <- {
        some code
    }
    Foo2 <- Foo + {
        some other code
    }
    ```
    In pythonic syntax, this is equivalent to
    ```python
    class Foo:
        # some code
    
    class Foo2(Foo):
        # some other code
    ```

    In the above example, `Foo2` imherits everything from `Foo`, while also adding its own specific implementations.

    Also since everything is a set, so functions can also inherit from other functions. The only requirement is that the parameter list must be the same for the function inheritance to take place.
    ```
    foo(a, b) <- {
        some code
    }
    foo2(a, b) <- foo(a, b) + {
        some other code
    }
    ```
    This is equivalent to 
    ```
    foo2(a, b) <- {
        some code,
        some other code
    }
    ```
    If the order of the addition is changed,
    ```
    foo2(a, b) <- {
        some other code
    } + foo(a, b)
    ```
    then the lines indented will also change its order
    ```
    foo2(a, b) <- {
        some other code,
        some code
    }
    ```
    (This only applies to function inheritance, but not to class inheritances.)