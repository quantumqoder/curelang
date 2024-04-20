# +

The $+$ operator double downs as summation function with variadic arguments as well, meaning $+(a, b, c, ...)\rightarrow \sum a$.

1. number1 + number2 -> addition
2. string1 + string2 -> concatenation (f"{string1}{string2}")
3. number + string -> addition if string is digit else {number, string}
4. string + number -> addition if string is digit else concatenation (f"{string}{number}")
5. sequence1 + sequence2 -> sequence extension ({*sequence1,*sequence2})
6. sequence + element (single line) -> sequence extension

# -

The $-$ operator double downs as subtraction function with two arguments as well, meaning $-(a, b)\rightarrow a-b$.

1. number1 - number2 -> subtraction
2. string1 - string2 -> string removal ("duck" - "ck" -> "du", "saas" - "s" -> "aa")
3. number - string -> subtraction if string is digit else nothing
4. string - number -> subtraction if string is digit else character removal ("666hell666" - 666 -> "hell")
5. sequence1 - sequence2 -> element removal ({1, 2, 4} - {1, 4} -> {2})
6. sequence - element (single line) -> element removal ({1, 2, 4} - 1 - 4 -> {2})

# *

The $*$ operator double downs as product function with variadic arguments as well, meaning $*(a, b, c, ...)\rightarrow \Pi~a$.

1. number1 * number2 -> multiplication
2. string1 *string2 -> pair product ("duck"* "ck" -> {"dc", "dk", "uc", "uk", ..., "ck", "kc", "kk"})
3. number *string -> multiplication if string is digit else string repeatition, number times (3* "ass" -> "assassass")
4. string *number -> string repeatition, number times ("ass"* 3 -> "assassass")
5. for other types, the operation needs to be explicitly defined

# /

The $/$ operator double downs as division function with two arguments as well, meaning $/(a, b)\rightarrow a/b$.

1. number1 / number2 -> floor division
2. string1 / string2 -> floor division if both strings are digits else truncate string ("duck" / "ck" -> "du", "saas" / "s" -> "saa")
3. number / string -> floor division if string is digit else truncate dtring from front (2 / "duck" -> "ck")
4. string / number -> truncate string by number ("duck" / 2 -> "du")
5. sequence / number -> truncate sequence by number

# Comment lines

`C(comment)`

# Assignment (=, {}, ())

`=`: evaluator\
`{}`: assinger and initializer\
`()`: initializer

# Callables (includes constructor functions, procedures, functions, properties)

In CURE, callables are the most important and fundamental entity around which the whole programming language is build. Everything is a callable and as well a sequence (more on this later). In different sitatuons, these callables can act as constructors, procedures, functions or even properties.

Constructors, in CURE, are callables which return an instance of the callable type.

Procedures are callable which also return an instance of callable type, but not assigned to any identifier. Basically, in CURE, there's no difference between a procedure and a constructor, if the call is aasigned, then the callable is a constructor, if the call is not assigned, then it's a procedure.

Functions are callables which return values. Pure functions can not be enforced, but can be implemented through proper design. Thus in CURE, callables are allowed to have side-effects.

Properties are properties. They are directly excuted without invoking, but can ve invoked as well. what'll happen in the following scenario??
`name(param1) = dump(param1)` `name` will dump param1, name = name will dump param, name(raj) = preet will dump raj, preet. meaning properties are callable first and then property.

Function overloading (Google - Function computer programming)

```cpp
double Area(double h, double w) { return h * w; }

double Area(double r) { return r * r * 3.14; }
```

```
Area {
    (h, w) = h * w,
    (r) = r * r * 3.14
}
```

Recognizable definitons of a callable unit

`[return-type] name(parameter-list) : initializer-list [=] {body}` -> generic\
`name(parameter-list) : initializer-list` -> abstract\
`name : initializer-list {body}` -> callable without any exposed parameter\
`name(parameter-list) {body}` -> callable with only exposed parameter\
`name {body}` -> callable without any exposed parameter or initialized parameter\
`name = return-value` -> property (immutable one-liner getter)\
`name(v) : __var{v} = __var` -> property (mutable one-liner getter and setter)\
`name(parameter-list) : initializer-list = {body, return(return-value)}` -> property (mutable multi-line getter and setter)\
`name(parameter-list) = return-value` -> pure function\
`(parameter-list) : initializer-list {body}` -> callable with file name (makes the file itself callable), anonymous function

The syntax for defining a callable unit contains five fields, all of which are optional. But, ommiting any of these fields changes the behaviour of the callable unit and notifies the compiler, how to treat the entity, or what operations are allowed for the entity. The operations which are not defined, but are expected of the callable unit will be ignored, until and unless, the developer provides a definition of the operation in the `body` of the callable unit.

- `return-type`: The return type of the callable is an optional field.
    | `return-type` | `return` | behaviour |
    | - | - | - |
    | absent | absent | the callable will always return the object of the type `name`. |
    | absent | present | the compiler automatically infers the return type of the callable unit. |
    | present | absent | the callable would return an object of the type `return-type`. |
    | present | present | the compiler will try to cast the `return-values` into the specified `return-type`. |

- `name`: Name of the callable unit. If not provided, the compiler will define the callable and immediately release the associated memory, if any external variable is not captured inside the `body` of the callable. If a call is made immediately after defining the unit, then a value is produced which contains information of the callable `body` but any memory associated with the callable itself is released.

- `parameter-list`: Now, since the callables also act as constructor units, they would require an ability to expose some parameters to the
Supprts all three assignment operators (`=`, `{}`, `()`). This is what gets exposed as an accessible interface of the function.
- `initializer-list`: From `:` to `{}`, everything is initializer list. So, abstracts can't have them. Supports only `{}`, `()` assignments. If `=` is used like `name(params) : inti1{1}, initt2 = 2, init3(3), {body}`, then `name` will become a callable entity returning always the value `2`. `init3(3)` will be treated as a function call and try to return a value. If it can't achieve that, then assigns the value `3` to `init3`. `{body}` will be treated as a non-accessible sequence. This defines the variables which are accessible inside the function but not accessible outside. Moreover, any variable declared in this list can not be left un-initialized. If no initialization is provided for a variable, then that variable is initialized with none.
- `body`:

Each callable always have `name`, `arguments`, `body`, `value` and `child` and supports the operations: `+`, `-`, `*`. They also contain the functions: `isdigit`, `length`.

Callable units are automatically asynchronous. A call to same unit within the same scope will make the call on an independent thread.

| Contructor function | Procedure | Function | Property |
| - | - | - | - |
| Returns an object of `name` type | Returns an object of `name` type | Returns the parameters of the in-built `return()` function | Returns the evaluated value or `body` depending on the type of assingment operator used |
| Should not contain `return()` call | Should not contain `return()` call | Should contain `return()` call | Doesn't require a `return()` call for one-liner; Should have a `return()` call for multi-liner |
! A constructor function's body should generally contain the fields, attributes and member methods as it returns the object itself | Similar to constructor functions, they can also contain all the things that any other callable could have. There is not restriction in what a callable can have or can't. | They generally should contain the functional logic and should not modify the states of object. Although again, it's not restricted by the interpreter. | The functional logic implemented must be assigned to the callable's signature. |

Question? what happens when `name(params) : inits = sequence` -> returns the sequence only when all elements are identities (callables which return themselves). In other words, each and every element is evaluated.

Supports multiple signatures as follows:-

```
    name {
        (params1) : inits1 {body1},
        (params2) : inits2 {body2},
        C(members common to both signatures)
    }
```

This type of multiple signatures supports parameter-based dynamic class definition. The whole class body changes depending on the parameters provided to the contructor function call.

## Comparison between function definition of different programming languages

C++

```cpp
    class Foo
    {
        int __foo;
    public:
        Foo() : __foo(0) {}; // default constructor
        Foo(const int foo) : __foo(foo) {}; // parameterized constructor
    }
```

Python

```python
    from typing import Self

    class Foo:
        __foo: int
        def __new__(cls, foo: int = 0) -> Self:
            return object.__init__(cls)

        def __init__(self, foo: int = 0) -> None:
            self.__foo: int = foo
```

JavaScript

```javascript
    class Foo {
        constructor(foo) {
            this.__foo = foo
        }
    }
```

CURE

```cure
    Foo {
        () : __foo{0} {},
        (foo) : __foo(foo) {}
    }
```

# Constructor Function definitions

This uses the javascript example on [this page](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes).

```
    Rectangle(height, weight) {}
```

```
    Rectangle = (height, weight) {}
```

```
    Rectangle = Rectangle2(height, weight) {}
```

The 3rd definition creates inheritance.

# Inheritance

## Without introducing any new members

C++

```cpp
    class Foo
    {
        int __foo;

    public:
        Foo(const int foo=0) : __foo(foo) {}
    };

    class Baz : public Foo
    {
    public:
        Baz() : Foo() {}
        Baz(const int foo) : Foo(foo) {}
    };
```

Python

```python
    class Foo:
        def __init__(self, foo: int=0) -> None:
            self.__foo = foo

    class Baz(Foo):
        ...
```

CURE

```cure
    Foo(foo) : __foo(foo) {},

    Baz = Foo
```

## With new members

C++

```cpp
    class Foo
    {
        int __foo;

    public:
        Foo(const int foo=0) : __foo(foo) {}
        int get_foo() const { return __foo; }
    };

    class Baz : public Foo
    {
        int __baz;
    public:
        Baz() : Foo(), __baz(0) {}
        Baz(const int baz) : Foo(), __baz(baz) {}
        Baz(const int foo, const int baz) : Foo(foo), __baz(baz) {}
        int get_baz() const { return __baz; }
    };
```

Python

```python
    from typing import Optional

    class Foo:
        def __init__(self, foo: int = 0) -> None:
            self.__foo = foo

        def get_foo(self) -> int:
            return self.__foo

    class Baz(Foo):
        def __init__(self, foo: int = 0, baz: Optional[int]=None) -> None:
            super().__init__(foo)
            self.__baz = baz or 0

        def get_baz(self) -> int:
            return self.__baz
```

CURE

```cure
    Foo(foo) : __foo(foo) {
        get_foo() = __foo
    },

    Baz = Foo + {
        () : Foo(0), __baz(0) {},
        (baz) : Foo(0), __baz(baz) {},
        (foo, baz) : Foo(foo), __baz(baz) {},
        get_baz() = __baz
    }
```

The same behaviour can be achieved by the unpack operation `*`.

```cure
    Foo(foo) : __foo(foo) {
        get_foo() = __foo
    },

    Baz {
        *Foo,
        () : Foo(0), __baz(0) {},
        (baz) : Foo(0), __baz(baz) {},
        (foo, baz) : Foo(foo), __baz(baz) {},
        get_baz() = __baz
    }
```

Types are optional, but when provided, it would enforce the type
Eveything is mutable.

`num x: char` means that the input must be a number which will be converted to character. both

All functions are dervied from CallableSequence, hence

```
    foo(a, b),

    dump("f{typeof(foo)=}") C(CallableSequence)
```

the logic is to define first and then use. this is for the difference between () asignment and () function call.
