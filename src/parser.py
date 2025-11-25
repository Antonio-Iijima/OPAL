def toPython(expr: str) -> list:
    """Convert parenthesized string syntax to Python list."""
    
    def convert(expr: list) -> list:
        """Convert intermediary list of strings into nested lists."""
        if expr == []: return expr
        elif expr[0] == "(":
            balance = 0
            for idx, char in enumerate(expr):
                if   char == "(": balance += 1
                elif char == ")": balance -= 1
                if balance == 0: return [convert(expr[1:idx]), *convert(expr[idx+1:])]
        return [expr[0], *convert(expr[1:])]
    
    return convert(expr.replace("(", " ( ").replace(")", " ) ").replace("'", " ' ").split()).pop()



tests = [
    "(+ 1 2)",
    "a",
    "(+ 1 (+ 3 4))",
    "((1 2) 3 (4 5))"
]

solutions = [
    ['+', '1', '2'],
    'a',
    ['+', '1', ['+', '3', '4']],
    [['1', '2'], '3', ['4', '5']],
]

for test, solution in zip(tests, solutions):
    print(toPython(test) == solution or toPython(test))
