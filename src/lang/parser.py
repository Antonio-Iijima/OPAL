"""Parser and basic syntax checker."""



from src.lang import interpreter as INT
from src.lang import keywords as KEY



##### Syntax checking and type conversions #####



## Basic syntax checking (parentheses, operators, etc.) and low-level processes


def iscommented(expr: str) -> bool:
    """Checks for single- or multiline comments."""
    return INT.interpreter.COMMENT_COUNTER or any(comment in expr for comment in (INT.interpreter.SINGLE_COMMENT, INT.interpreter.MULTILINE_COMMENT_OPEN, INT.interpreter.MULTILINE_COMMENT_CLOSE))


def iscomplete(expr: str) -> bool:
    """Checks for *hopefully* complete expressions in the REPL."""
    
    # Filter expressions that will never complete
    if expr.count(")") > expr.count("("): raise SyntaxError(f"fatal expression: {" ".join(expr)}")
    
    return all(ext in expr for ext in ("@start", "@end")) or ("@start" not in expr and expr.count("(") == expr.count(")"))


def isperfectlybalanced(expr: list) -> bool: 
    """Check for balanced parentheses in an OPAL expression."""
    
    stack = 0

    for char in expr:
        if char == "(": stack += 1
        elif char == ")": 
            if not stack: raise SyntaxError(f"unmatched closing parenthesis in {" ".join(expr)}")
            else: stack -= 1
    
    if stack: raise SyntaxError(f"unmatched opening parenthesis in {" ".join(expr)}")


def syntax_check(expr: list) -> list:
    """Checks balanced parentheses, proper expression nesting, etc. Raises errors if any conditions not met, otherwise returns `expr`."""

    isperfectlybalanced(expr)        

    return expr


def retype(x: str) -> int | float | bool: 
    """Replace int, float, and bool strings with their correct data types."""

    return (
        (float(x) if "." in x else int(x)) if KEY.isnumber(x)
        else x == "#t" if x in ("#t", "#f")
        else x
    )


def preprocess(expr: list) -> list:
    """Replace all special data types."""

    return (
        [] if expr == []
        else [preprocess(expr[0]), *preprocess(expr[1:])] if isinstance(expr[0], list)  # Process the head and the tail
        else [["quote", preprocess(expr[1])], *preprocess(expr[2:])] if expr[0] == "'"  # Expand ' syntax to full (quote x) expressions
        else [retype(expr[0]), *preprocess(expr[1:])]                                   # Otherwise replace with correct data type
    ) if isinstance(expr, list) else expr
 


##### Complete OPAL <-> Python converters #####



def toPython(expr: str) -> list:
    """Convert OPAL syntax to Python list."""
    
    def convert(expr: list) -> list:
        """Convert intermediary list of strings into nested lists."""
        if expr == []: return expr
        elif expr[0] == "(":
            balance = 0
            for idx, char in enumerate(expr):
                if   char == "(": balance += 1
                elif char == ")": balance -= 1
                if balance == 0: i = idx; break      
            return [convert(expr[1:i]), *convert(expr[i+1:])]
        return [expr[0], *convert(expr[1:])]
    
    return convert(expr.replace("(", " ( ").replace(")", " ) ").replace("'", " ' ").split()).pop()


def toOPAL(s: any) -> str | None:
    """Convert Python list to fully-parenthesized OPAL string."""

    return (
        None if s is None
        else ("#t" if s else "#f") if isinstance(s, bool)
        else f"'{toOPAL(s[1])}" if KEY.isquote(s) 
        else f"({' '.join(toOPAL(elem) for elem in s if elem != None)})" if isinstance(s, list) 
        else str(s)
    )


def parse(s: str) -> list: 
    """Perform syntax checking and convert OPAL expression string to manipulable Python lists."""
    return preprocess(syntax_check(toPython(s)))
