"""General built-in functions."""



def append(x: list, y: list) -> list:
    """Return the concatenation of `x` and `y`."""
    return x + y


def cons(x: any, y: list) -> list:
    """Return a list where `x` is the head and `y` is the tail."""
    return [x] + y


def show(expr: str) -> None:
    """Prints to standard output."""
    print(PAR.toALVIN(expr))


def usrin(expr: list) -> str:
    """Reads from standard input."""
    return input(f"{expr} ") # pragma: no cover


def elem(x: any, y: list | str) -> bool:
    """List and string membership function."""
    return x in y


def ref(l: list, i: int) -> any:
    """List indexing."""
    return l[i]
    

def setref(l: list, i: int, item: any) -> None:
    """Replace the existing contents of `l` at index `i` with `item`."""
    l[int(i)] = item


def evlist(x: list) -> list:
    """Evaluates each element in the input list and returns them as a list."""
    return [*map(EVA.evaluate, x)]


def head(x: list) -> any:
    """Returns the head of a list or raises a TypeError."""
    try: return x[0]
    except: raise TypeError(f"unsupported argument for 'car': {PAR.toALVIN(x)}")


def tail(x: list) -> list:
    """Returns the tail of a list or raises a TypeError."""
    try: return x[1:]
    except: raise TypeError(f"unsupported argument for 'cdr': {PAR.toALVIN(x)}")
    

def evcxr(x: str, output: list) -> any:
    """Tail-recursive evaluation of `cxr` expressions (arbitrary combinations of `car` and `cdr`)."""

    if not x: return output
    elif x.endswith("a"): return evcxr(x.removesuffix("a"), head(output))
    elif x.endswith("d"): return evcxr(x.removesuffix("d"), tail(output))


def rebool(x: str | bool) -> bool:
    """Convert the literal `#t` and `#f` into the `bool` datatype."""
    return x == "#t" if isinstance(x, str) else x


def lst(*x: str | int | bool) -> list:
    """List type conversion."""
    return list(x)
