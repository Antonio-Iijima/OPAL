"""Evaluation function."""



import config as cf
import keywords as kw
import datatypes as dt



##### Expression Evaluation #####



def evaluate(expr: any) -> any:
    """Evaluates complete OPAL expressions."""
   # print(expr)
    # Processing a single atom

    # Look up variables, return literals
    if kw.isatom(expr): return (
        cf.config.ENV.lookup(expr) if kw.isvariable(expr)
        else kw.rebool(expr) if kw.isbool(expr)
        else expr
    )
    
    # Otherwise processing a list

    # Empty list
    elif kw.isnull(expr): return []

    # Head is an atom
    elif kw.isatom(expr[0]):

        # Head and tail identifiers for readability
        HEAD, *TAIL = expr

        # Evaluate methods from imported modules
        if kw.isimport(HEAD): return kw.run_method(HEAD, TAIL)

        # Evaluate function calls and lazy wrappers
        elif isinstance(HEAD, (
            dt.Function, 
            dt.Template, 
            dt.Instance, 
            dt.Lazy
        )): return HEAD.eval(TAIL)

        # If the head is a variable, replace it with its value and re-evaluate the expression
        elif kw.isvariable(HEAD): return evaluate([cf.config.ENV.lookup(HEAD), *TAIL])

        # If its a keyword, evaluate each group
        elif kw.iskeyword(HEAD):
            for NAME, CATEGORY in cf.config.KEYWORDS.items():
                if HEAD in CATEGORY:
                    match NAME:

                        # Regular or applicative-order n-ary functions
                        case "REGULAR": return CATEGORY[HEAD](*kw.evlist(TAIL))

                        # Irregular or normal-order n-ary functions
                        case "IRREGULAR": return CATEGORY[HEAD](*TAIL)

                        # Environment manipulation functions
                        case "ENVIRONMENT": return CATEGORY[HEAD](*TAIL)

                        # Boolean functions
                        case "BOOLEAN": return CATEGORY[HEAD](*map(bool, kw.evlist(TAIL)))

                        # Extensions
                        case "EXTENSIONS": return CATEGORY[HEAD](*TAIL)

            # 'cxr' expressions
            if kw.iscxr(HEAD): return kw.evcxr(HEAD[1:-1], evaluate(expr[1]))

            # Special forms and functions with unique evaluation requirements
            match HEAD:

                # Lazy parameter evaluation wrapper for functions
                case "lazy": return dt.Lazy(*TAIL)

                # Create new template instances
                case "new" : return cf.config.ENV.lookup(TAIL[0]).new(*TAIL[1:]) 

                # Evaluate 'until' expressions
                case "until": return kw.until(expr[1][0], expr[1][1], expr[2])

                # Lambda function declarations
                case "lambda": return dt.Function("lambda", expr[1], expr[2])

                # 'string' and 'list' predicates
                case "string?": return kw.isstring(TAIL)
                case "list?":  return kw.islist(TAIL)

                # Evaluate conditionals
                case "cond": return kw.cond(TAIL)

                # Evaluate 'quote' expressions
                case _: return expr[1]
        
        # Otherwise head is a literal
        return kw.evlist(expr)

    # Otherwise head is a list
    evaluated = [evaluate(expr[0]), *expr[1:]]; return expr if expr == evaluated else evaluate(evaluated)
