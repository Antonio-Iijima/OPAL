"""Evaluation function."""



import config as cf
import keywords as kw
import datatypes as dt



##### Expression Evaluation #####



def evaluate(expr):
    """Evaluates complete OPAL expressions."""

    # Processing a single atom

    # Look up variables in environment, otherwise return as literal
    if kw.isatom(expr): return cf.config.ENV.lookup(expr) if kw.isvariable(expr) else kw.rebool(expr) if kw.isbool(expr) else expr

    # Otherwise processing a list

    # Empty list
    elif kw.isnull(expr): return []

    # Head is an atom
    elif kw.isatom(expr[0]):

        # Head and tail identifiers for readability
        HEAD, TAIL = expr[0],  expr[1:]

        # Evaluate methods from imported modules
        if kw.isimport(HEAD): return kw.run_method(HEAD, TAIL)

        # Evaluate function calls
        elif kw.isfunction(HEAD): return HEAD.eval(TAIL)

        # Evaluate templates
        elif kw.istemplate(HEAD): return HEAD.eval(*TAIL)
        
        # If the head is a variable, replace it with its value and re-evaluate the expression
        elif kw.isvariable(HEAD): return evaluate([cf.config.ENV.lookup(HEAD), *TAIL])

        # If its a keyword, evaluate each group
        elif kw.iskeyword(HEAD):
            
            # Regular or applicative-order n-ary functions
            if HEAD in kw.REGULAR: return kw.REGULAR[HEAD](*kw.evlist(TAIL))

            # Irregular or normal-order n-ary functions
            elif HEAD in kw.IRREGULAR: return kw.IRREGULAR[HEAD](*TAIL)

            # Environment manipulation functions
            elif HEAD in cf.config.ENVIRONMENT: return cf.config.ENVIRONMENT[HEAD](*TAIL)

            # Boolean functions
            elif HEAD in kw.BOOLEAN: return kw.BOOLEAN[HEAD](*[bool(arg) for arg in kw.evlist(TAIL)])

            # Extensions
            elif HEAD in cf.config.EXTENSIONS: return cf.config.EXTENSIONS[HEAD](*TAIL)

            # 'cxr' expressions
            elif kw.iscxr(HEAD): return kw.evcxr(HEAD[1:-1], evaluate(expr[1]))

            # Special forms and functions with unique evaluation requirements
            match HEAD:

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
