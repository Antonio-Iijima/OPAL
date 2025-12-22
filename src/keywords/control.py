"""Control flow functions."""


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
