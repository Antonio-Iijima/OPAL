"Predicates for internal and external use."



from src.lang  import interpreter as INT
from src.lang import datatypes as DAT

import re



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


def isfunction(x: "DAT.Function") -> bool: 
    """Unary `Function` predicate."""
    return isinstance(x, DAT.Function)


def istemplate(x) -> bool:
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


def isfrozen(x: "DAT.Frozen") -> bool: 
    """Unary `Frozen` predicate."""
    return isinstance(x, DAT.Frozen)


def islazy(x: "DAT.Lazy") -> bool: 
    """Unary `Frozen` predicate."""
    return isinstance(x, DAT.Lazy)
