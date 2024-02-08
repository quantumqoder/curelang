```cpp
#include <iostream>
#include <string>

class Foo
{
    int __foo;
    int __bar;

public:
    Foo(const int foo) : __foo(foo), __bar(0) {}
    Foo(const int foo, const int bar) : __foo(foo), __bar(bar) {}
    void view_foo() { std::cout << __foo << std::endl; }
    void view_foobar() { std::cout << __foo << ", " << __bar << std::endl; }
    const int foo() const { return __foo; }
    const int bar() const { return __bar; }
    void bar(const int bar) { __bar = bar; }
    std::string str() { return std::to_string(__foo) + ", " + std:to_string(__bar); }
    std::string repr() { return "Foo(" + Foo::str() + ")"; }
    Foo operator() () { return Foo(__foo, this.bar); }
};

class Baz : public Foo
{
    int __baz;

public:
    Baz() : Foo(0), __baz(0) {}
    Baz(const int baz) : Foo(0), __baz(baz) {}
    Baz(const int foo, const int baz) : Foo(foo), __baz(baz) {}
    Baz(const int foo, const int bar, const int baz) : Foo(foo, bar), __baz(baz) {}
    Baz(const Foo& foo, const int baz) : Foo(foo->foo, foo->bar), __baz(baz) {}
    const auto baz() const { return __baz; }
    void baz(const int baz);
    std::string str() { return Foo::str() + ", " + std::to_string(this.baz); }
    std::string repr() { return "Baz(" + Baz::str() + ")"; }
    Baz operator() () { return Baz(__for, __bar, __baz); }
};

void Baz::baz(const int baz)
{
    switch(baz)
    {
        case __foo:
            __baz = __foo;
        break;
        case __bar:
            __baz = __bar;
        break;
        default:
            __baz = baz;
    }
};

Foo make_foo(const int foo, const int bar=0)
{
    return (bar != 0) ? Foo(foo, bar) : Foo(foo);
};

Baz make_baz(const int foo, const int bar, const int baz)
{
    return Baz(make_foo(foo, bar), baz)
};

int main()
{
    Foo foo_obj = make_foo(2);
    std::cout << foo_obj.bar << std::endl; // prints 0 in standard output
};
```

```python
from typing import Optional

class Foo:
    def __init__(self, foo: int, bar: int=0) -> None:
        self.__foo = foo
        self.__bar = bar

    def view_foo(self) -> None:
        print(self.__foo)

    def view_foobar(self) -> None:
        print(f"{self.__foo=}, {self.__bar=}")

    @property
    def foo(self) -> int:
        return self.__foo

    @property
    def bar(self) -> int:
        return self.__bar

    @bar.setter
    def bar(self, bar: int) -> None:
        self.__bar = bar

    def __str__(self) -> str:
        return f"{self.__foo=}, {self.__bar=}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"

    def __call__(self) -> Foo:
        return (self.__class__(self.__foo, self.bar, self.__baz)
                if hasattr(self, "__baz")
                else self.__class__(self.__foo, self.__bar))

class Baz(Foo):
    def __init__(self, foo: int=0, bar: int=0, baz: int=0) -> None:
        if isinstance(foo, Foo):
            super().__init__(foo.foo, foo.bar)
            self.__baz = bar
        else:
            super().__init__(foo, bar)
            self.__baz = baz

    @property
    def baz(self) -> int:
        return self.__baz

    @baz.setter
    def baz(self, baz: int) -> None:
        match baz:
            case self.__foo:
                self.__baz = self.__foo
            case self.__bar:
                self.__baz = self.__bar
            case _:
                self.__baz = baz

    def __str__(self) -> str:
        return f"{Foo.__str__(self)}, {self.baz=}"

def make_foo(foo: int, bar: Optional[int]=None) -> Foo:
    return Foo(foo, bar) if bar else Foo(foo)

def make_baz(foo: int, bar: int, baz: int) -> Baz:
    return Baz(make_foo(foo, bar), baz)

foo_obj: Foo = make_foo(2)
print(foo_obj.bar) # prints 0 in standard output
```

```
Foo {
    (foo) : __foo(foo) {},
    (foo, bar) : __foo(foo), __bar(bar) {
        view_foobar {
            dump(f"{__foo=}, {__bar=}")
        }
    },
    view_foo { dump(__foo) },
    foo = __foo,
    bar : __bar(bar) = __bar,
    dump = f"{__foo=}, {__bar=}",
    repr {
        return(f"{.name}, {.dump}")
    },
    () = __baz ? .(__foo, .bar, __baz) : .(__foo, __bar) C(This may seem to override the construction behaviour, but recall that constructors do not have any `return()` call or expression assignment. They've either empty body or methods defined in them.)
},

Baz = Foo + {
    () {},
    (baz) : __baz(baz) {},
    (foo, baz) : Foo(foo), __baz(baz) {},
    (foo, bar, baz) : Foo(foo, bar), __baz(baz) {},
    (Foo foo, baz) : Foo(foo.foo, foo.bar), __baz(baz) {},
    baz : __baz(baz) = baz ? {
        (__foo) : __foo,
        (__bar) : __bar
    } : {
        baz
    },
    dump = f"{Foo.dump()}, {.baz=}"
},

Foo make_foo(foo, bar=) = bar ? Foo(foo, bar) : Foo(foo),

Baz make_baz(foo, bar, baz) = Baz(make_foo(foo, bar), baz),

foo_obj{make_foo(2)},
dump(foo_obj.bar) C(prints nothing in standard output. The logic is "you get what you give. you get nothing if you give nothing."),
dump(foo_obj.foo) C(prints 2 in standard output.),
foo_obj.foo = 5 C(prints "Warning: Definition of foo_obj.foo is overwritten by foo_obj.foo = 5" at standard error.),
foo_obj.bar = 3 C(defines __bar in foo_obj and initializes it with value 3. Unlike the former case, this is possible iff either the `parameter-list` or the `initializer-list` is provided.),
dump(foo_obj.bar) C(prints 3 in standard output.),
dump(foo_obj.bar()) C(prints 3 in standard output.),
foo_obj.bar(7) C(sets the value of __bar to 7.)
foo_obj.bar() = 7 C(prints "Warning: Definition of foo_obj.bar is overwritten by foo_obj.bar() = 7" at standard error.)
```

`[return-type] name(params) : init {}`: .name is treated as property. name() is treated as function call.