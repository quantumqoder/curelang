# LANGUAGE SYNTAX

# Comment Lines (both in-line and block)
    -:<comment-body>:-

# Import Statements
## Module import
    "<module-name>"
## Class import
    "<module-name.class-name>"
## Function import
    "<module-name.function-name>"
## Class Function import
    "<module-name.class-name.function-name>"

# Data Types
## Non-Empty Set
Includes integers, non-integers, complex, quaternions, ...  
1, 1.5, 1+i, 1+i+j+k, 1+e0+e1+e2+e01+e02+e12+e012, ...
## Undefined
basically everything else; strings, character, class, functions, modules
## Empty Set
basically, None, void, [], {}, anything which is empty.  
"Empty" is always mutable, since something defined empty can have a value or element assigned to it at a later point during execution.

# Variable declaration
    <variable-name>
Whenever a variable is declared, it, by default is assigned an empty type. Writing explicitly, <variable-name\> <- Empty is also a valid implementation. 
# Varaible assignment
    <variable-name> <- <value>
# Varaible Scope
Same as the variable scopes in other languages

# Operators
## Addition
    +
## Subtraction
    -
## Multiplication
    *
## Division
### Float Division
    /
### Integer Division
    /.
    
## Assingment
    <-
## Injection
(For injecting code blocks into pre-defined code blocks)
```
    ->
```

```
Foo <- {
    some code
}
{
    some other code
} -> Foo
```

This is equivalent to
```
Foo <- {
    some code,
    some other code
}
```
Now, this may lead to security issues and creators may not want to inject code later. For that, the protect keyword can be used.
```
protect Foo <- {
    some code
}
{
    some other code
} -> Foo -: throws a NoInjectionError :-
```
Although, the class can also be protected adter the class has been defined.
```
Foo <- {
    some code
}
{
    some other code
} -> Foo -: does not throw an error :-
protect Foo
{
    some more code
} -> Foo -: throws an error :-
```

# Classses and Functions (or, Methods)
In Mpl, there's no distinction between classes and functions (or methods). Both of them follow exactly the same definition pattern, and are referred to as code blocks. Rather, there're no classes in MPL. The blueprint of the object, known as the class, is actually a singleton object. Refer to Class Def section.

```
<name> <- {
    var1, var2, var3, ..., -: Initial object variables. They're defaulted to empty, but can be assigned user-default values :-
    [var4, var5, var6, ...], -: Available only after constructor calls. The constructor need no to defined and not all needs to assigned during conrtuction :-
    value1, value2, value3, ..., -: the code block can also hold values, accessible through <name>.values. These'll be in the order of how they're mentioned :-
    <func>, -: automaitcally binds this with <name> :-
    <func1> <- {
        param1, param2, ...,
        line1,
        line2,
        line3,
        param2, param1 -: these values are returned in the same order they're mentioned :-
    }
    line3, -: these're excuted as normal function call :-
    line4,
    line5
}
```

# Function Def
```
<fucntion-name> <- {
    param1, param2, ...,
    <function-body>,
    return-list // Optional
}
```

Default values can be provided by
```
<function-name> <- {
    param1, param2 <- default-value,
    <function-body>,
    return-list -: Optional :-
}
```

# Class Def
```
<class-name> <- {
    var1, var2 <- default-value, var3, ...,
    [var4 <- default-value, var5, ...] <- {
        contructor body -: optional constructor body :-
    },
    <function-name> <- {
        param1, param2 <- default-value, param3, ...,
        <function-body>,
        return-parameters -: optional :-
    },
    <func> -: automaitcally binds <func> with <class-name>, accessible through <class-name>.<func> :-
}
```

# Inheritance
Classes can be extended as follows
```
<class-name> <- {
    class_variable1, class-variable2 <- value,
    some code
} + <base-class>
```
This is also equivalent to
```
<class> <- <base-class> + {
    var1, var2 <- val,
    some code
}
```

By the same notation functions can also be extended or inherited.
```
<function-name> <- {
    parameter1, parameter2 <- value,
    <function-body>,
    return-list // Optional
} + <class>.<function>
```
In situations as follows, the function is automatically bound to the class and it's object. (Note that this is different from function compositon.)
```
<class> <- {
    some code
}
<func> <- {
    some other code
}
<func> -> <class> -: injects the <func> into <class>. can be accessed as <class>.<func> :-
<func>, -> <class> -: injects lines of codes in <func> into <class> :-
```
`<func> -> <class>` is equivalent to
```
<class> <- {
    some code,
    <func> <- {
        some other code
    }
}
```
`<func>, -> <class>` is equivalent to
```
<class> <- {
    some code,
    some other code
}
```