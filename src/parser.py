"""Parser and basic syntax checker."""



import config as cf
import keywords as kw



##### Syntax checking and type conversions #####



## Basic syntax checking (parentheses, operators, etc.) and low-level processes


def iscomment(expr: str) -> bool:
    """Checks for single- or multiline comments."""
    return cf.config.COMMENT_COUNTER or any(comment in expr for comment in (cf.config.SINGLE_COMMENT, cf.config.MULTILINE_COMMENT_OPEN, cf.config.MULTILINE_COMMENT_CLOSE))


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

    if kw.isnumber(x): return float(x) if "." in x else int(x)
    elif x in ("#t", "#f"): return x == "#t"
    return x


def preprocess(expr: list) -> list:
    """Replace all special data types."""

    # Filter only expressions
    if isinstance(expr, list):
        if expr == []: return []
        
        # Process the head and the tail
        elif isinstance(expr[0], list): return [preprocess(expr[0]), *preprocess(expr[1:])]
        
        # Expand ' abbreviation to full (quote x) expressions
        elif expr[0] == "'": return [["quote", preprocess(expr[1])], *preprocess(expr[2:])]

        # Otherwise replace with correct data type
        return [retype(expr[0]), *preprocess(expr[1:])]

    # Otherwise return original input atom
    return expr



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

    if s == None: return None
    elif isinstance(s, bool): return "#t" if s else "#f"

    # Otherwise replace lists with parentheses and (quote x) with '
    return f"'{toOPAL(s[1])}" if kw.isquote(s) else f"({' '.join(toOPAL(elem) for elem in s if elem != None)})" if isinstance(s, list) else str(s)


def parse(s: str) -> list: 
    """Perform syntax checking and convert OPAL expression string to manipulable Python lists."""
    return preprocess(syntax_check(toPython(s)))
