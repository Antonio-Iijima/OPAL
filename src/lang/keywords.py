"""OPAL Builtin Functions"""



import re
import importlib

import repl as REP
import parser as PAR
import evaluate as EVA
import datatypes as DAT
import interpreter as INT



##### Functions #####



## Predicates for internal and/or external use


def isquote(x: str) -> bool: 
    """Unary `quote` expression predicate."""
    return isinstance(x, list) and len(x) == 2 and x[0] == "quote"


def isvariable(x: str) -> bool:
    """Unary `variable` predicate."""
    return isatom(x) and not(iskeyword(x) or isnumber(x) or isbool(x))

    
def iskeyword(x: str) -> bool: 
    """Unary `keyword` predicate."""
    return any(x in category for category in INT.interpreter.KEYWORDS.values()) or iscxr(x)


def isimport(x: str) -> bool:
    """Unary `import` predicate."""
    return bool(re.match(r"^[a-z, A-Z]*[.][a-z, A-Z]+$", str(x)))


def isnumber(x: str | int | float) -> bool: 
    """Unary `int` or `float` predicate."""
    return bool(re.match(r"^[-]?[0-9]*[.]?[0-9]+$", str(x)))


def isint(x: str | int | float) -> bool: 
    """Unary `int` predicate."""
    return bool(re.match(r"^[-]?[0-9]*$", str(x)))


def isfloat(x: str | int | float) -> bool: 
    """Unary `float` predicate."""
    return bool(re.match(r"^[-]?[0-9]*[.][0-9]+$", str(x)))


def isfunction(x: DAT.Function) -> bool: 
    """Unary `Function` predicate."""
    return isinstance(x, DAT.Function)


def istemplate(x: DAT.Template | DAT.Instance) -> bool:
    """Unary `Template` and `Instance` predicate."""
    return isinstance(x, (DAT.Template, DAT.Instance))


def iscxr(x: str) -> bool:
    """Unary `car` and `cdr` predicate, generalized to include all abbreviated forms."""
    return bool(re.match(r"^c[ad]+r$", str(x)))


def isatom(x: any) -> bool:
    """Unary `atom` predicate."""
    return not isinstance(x, list)

    
def isnull(x: list) -> bool:
    """Unary `null` predicate."""
    return x == []


def isbool(x: str) -> bool:
    """Unary `bool` predicate."""
    return isinstance(x, bool) or x in ("#t", "#f")


def islist(x: list) -> bool:
    """Unary `list` predicate."""
    return (isquote(x) and isinstance(x[1], list)) or isinstance(x, list)


def isstring(x: list) -> bool:
    """Unary `string` predicate."""
    return isquote(x) or isinstance(x, str)


def isfrozen(x: DAT.Frozen) -> bool: 
    """Unary `Frozen` predicate."""
    return isinstance(x, DAT.Frozen)


def islazy(x: DAT.Lazy) -> bool: 
    """Unary `Frozen` predicate."""
    return isinstance(x, DAT.Lazy)


## Other basic functions


def append(x: list, y: list) -> list:
    """Return the concatenation of `x` and `y`."""
    return x + y


def cons(x: any, y: list) -> list:
    """Return a list where `x` is the head and `y` is the tail."""
    return [x] + y


def show(expr: str) -> None:
    """Prints to standard output."""
    print(PAR.toOPAL(expr))


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
    except: raise TypeError(f"unsupported argument for 'car': {PAR.toOPAL(x)}")


def tail(x: list) -> list:
    """Returns the tail of a list or raises a TypeError."""
    try: return x[1:]
    except: raise TypeError(f"unsupported argument for 'cdr': {PAR.toOPAL(x)}")
    

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


## More complex functions and special forms


def cond(expr: list) -> any:
    """Evaluate conditional expression."""
    
    # Evaluate the body of the conditional if the condition is true or 'else', otherwise move to next conditional
    return EVA.evaluate(expr[0][1]) if (expr[0][0] == "else" or EVA.evaluate(expr[0][0])) else cond(expr[1:])


def repeat(number: int, body: list) -> None:
    """Evaluate `body` `number` times."""
    
    n = EVA.evaluate(number)
    for _ in range(n):
        EVA.evaluate(body)


def until(cond: list | bool, inc: list, body: list) -> None:
    """Repeatedly evaluate.evaluate `body` until `cond` is `#f`. Runs in a local scope."""

    def logic(cond: list | bool, inc: int, body: list) -> None:
        while not(EVA.evaluate(cond)):
            EVA.evaluate(body)
            EVA.evaluate(inc)

    return INT.interpreter.ENV.runlocal(logic, cond, inc, body)


def let(bindings: list, body: list) -> any:
    """Binds all variables in `bindings` and evaluates `body` in a local scope."""

    def logic(bindings: list, body: list) -> any:
        for pair in bindings: INT.interpreter.ENV.set(*pair)
        return EVA.evaluate(body)
    
    return INT.interpreter.ENV.runlocal(logic, bindings, body)


def do(exprlist: list, body: list) -> any:
    """Evaluates a series of expressions before returning the value of `body`. Runs in a local scope."""
    
    def logic(exprlist: list, body: list) -> any:
        for expr in exprlist: EVA.evaluate(expr)
        return EVA.evaluate(body)
    
    return INT.interpreter.ENV.runlocal(logic, exprlist, body)


def OPAL_eval(expr: any) -> any:
    """Interpreter access from the command line for quoted expressions."""
    return EVA.evaluate(expr[1])


def getfile(filepath: str) -> list:
    """File system access."""
    return open(filepath).readlines()


def import_lib(name: str, _as: str = None, alias: str = None) -> None:
    """Import a library with an optional alias."""

    alias = alias or name
    name = importlib.import_module(name)
    INT.interpreter.IMPORTS[alias] = name


def load(location: str) -> None:
    """Load and run a .op file from provided relative location."""

    # Require .op files for reliability
    if not location.endswith(".op"): raise IOError(f"ensure file extension is *.op.")
    
    with open(location, "r") as file: REP.REPL(file.read().split("\n"), True)


def run_method(imported: str, args: list) -> any:
    """Call a method from an imported module or library."""

    module, method = imported.split(".")

    # Use the module and method strings to get the callable function
    imported = getattr(INT.interpreter.IMPORTS[module], method)

    # Either call the function with arguments or return it if none are provided
    return imported(*args) if callable(imported) else imported


def globals(var: str, val: any = None) -> None:
    """Define or access global variables."""

    # If val is provided, evaluate and assign it to var in the GLOBALS dictionary
    if val: INT.interpreter.GLOBALS[var] = EVA.evaluate(val)

    # Otherwise look up and return the value of var if it exists
    else: return INT.interpreter.GLOBALS.get(var, ValueError)


## Wrappers or slight extensions for basic Python functions
## Simplicity obviates the need for detailed comments or type annotation


# Mathematical functions
def eq(x, y)       : return x == y
def uneq(x, y)     : return x != y
def exponent(x, y) : return x ** y
def leq(x, y)      : return x <= y
def geq(x, y)      : return x >= y
def i_divide(x, y) : return x // y
def less(x, y)     : return x < y
def greater(x, y)  : return x > y
def multiply(x, y) : return x * y
def f_divide(x, y) : return x / y
def add(x, y)      : return x + y
def subtract(x, y) : return x - y
def mod(x, y)      : return x % y
def increment(x)   : return x + 1

# Boolean logic functions

def NOT(a)     : return not a
def OR(a, b)   : return a or b
def AND(a, b)  : return a and b
def XOR(a, b)  : return a is not b
def NOR(a, b)  : return not (a or b)
def NAND(a, b) : return not (a and b)



##### Collections #####



# Common applicative-order functions 
REGULAR = {
    "len"     : len,        "sort"  : sorted,
    "show"    : show,       "eq"    : eq,
    "+"       : add,        "-"     : subtract,
    "*"       : multiply,   "/"     : f_divide,
    "**"      : exponent,   "//"    : i_divide,
    ">"       : greater,    "<"     : less,    
    ">="      : geq,        "<="    : leq,
    "!="      : uneq,       "%"     : mod,
    "append"  : append,     "elem"  : elem,
    "=="      : eq,         "ref"   : ref,
    "null?"   : isnull,     "atom?" : isatom,
    "number?" : isnumber,   "cons"  : cons,
    "setref"  : setref,     "++"    : increment,
    "bool?"   : isbool,     "list"  : lst,
    "usrin"   : usrin
}


# Semi-normal-order functions; arguments are evaluated when necessary or not at all
IRREGULAR = {
    "repeat"  : repeat,       "let"     : let,          
    "do"      : do,           "eval"    : OPAL_eval,   
    "getfile" : getfile,      "global"  : globals,      
    "import"  : import_lib,   "load"    : load, 
    "list?"   : islist,       "string?" : isstring
}


# Boolean operations convert their arguments to boolean values before executing
BOOLEAN = {
    "and"  : AND,   "or"  : OR,
    "nor"  : NOR,   "xor" : XOR,
    "nand" : NAND,  "not" : NOT,
}


# Set of all special forms and other functions having 
# evaluation strategies handled explicitly by evaluate()
SPECIAL = { "lambda", "until", "string?", "list?", "cond", "quote", "new", "lazy", "set" }
