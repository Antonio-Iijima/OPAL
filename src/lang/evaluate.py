"""Evaluation function."""



from src.lang  import interpreter as INT
from src.lang import datatypes as DAT
from src.lang import keywords as KEY



##### Expression Evaluation #####



def evaluate(expr: any) -> any:
    """Evaluates complete OPAL expressions."""

    # Processing a single atom

    # Look up variables, return literals
    if KEY.isatom(expr): return (
        INT.interpreter.ENV.lookup(expr) if KEY.isvariable(expr)
        else KEY.rebool(expr) if KEY.isbool(expr)
        else expr
    )
        
    # Otherwise processing a list

    # Empty list
    if KEY.isnull(expr): return []
    
    # Head and tail identifiers for readability
    HEAD, *TAIL = expr

    # Head is an atom 
    if KEY.isatom(HEAD):

        # Evaluate methods from imported modules
        if KEY.isimport(HEAD): return KEY.run_method(HEAD, TAIL)

        # Evaluate function calls and lazy wrappers
        elif isinstance(HEAD, (
            DAT.Function, 
            DAT.Template, 
            DAT.Instance, 
            DAT.Lazy
        )): return HEAD.eval(TAIL)

        # If the head is a variable, replace it with its value and re-evaluate the expression
        elif KEY.isvariable(HEAD): return evaluate([INT.interpreter.ENV.lookup(HEAD), *TAIL])

        # If its a keyword, evaluate each group
        elif KEY.iskeyword(HEAD):
            for NAME, CATEGORY in INT.interpreter.KEYWORDS.items():
                if HEAD in CATEGORY and NAME not in "SPECIAL":
                    return CATEGORY[HEAD](*KEY.evlist(TAIL) if NAME in ("REGULAR", "BOOLEAN") else TAIL)

            # 'cxr' expressions
            if KEY.iscxr(HEAD): return KEY.evcxr(HEAD[1:-1], evaluate(expr[1]))

            # Special forms and functions with unique evaluation requirements
            match HEAD:

                case "set": return INT.interpreter.ENV.set(
                    TAIL[0], 
                    evaluate(TAIL[1]), 
                    INT.interpreter.ENV.find_scope(TAIL[0])
                )

                # Lazy parameter evaluation wrapper for functions
                case "lazy": return DAT.Lazy(*TAIL)

                # Freeze expressions for lazy evaluation
                case "freeze": return DAT.Frozen(*TAIL)

                # Create new template instances
                case "new": return INT.interpreter.ENV.lookup(TAIL[0]).new(*TAIL[1:]) 

                # Evaluate 'until' expressions
                case "until": return KEY.until(expr[1][0], expr[1][1], expr[2])

                # Lambda function declarations
                case "lambda": return DAT.Function("lambda", expr[1], expr[2])

                # Evaluate conditionals
                case "cond": return KEY.cond(TAIL)

                # Evaluate 'quote' expressions
                case "quote": return expr[1]
        
        # Otherwise head is a literal
        return KEY.evlist(expr)

    # Otherwise head is a list
    evaluated = [evaluate(HEAD), *TAIL]; return expr if expr == evaluated else evaluate(evaluated)
