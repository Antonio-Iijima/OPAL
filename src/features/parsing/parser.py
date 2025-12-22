class Parser:

    def parser_in(self, expr: str) -> list|str:
        """Convert OPAL to Python syntax."""
        return self._convert(expr.replace("(", " ( ").replace(")", " ) ").replace("'", " ' ").split()).pop()

    
    def _convert(self, expr: list) -> list:
        """Convert intermediary list of strings into nested lists."""
        if expr == []: return expr
        elif expr[0] == "(":
            balance = 0
            for idx, char in enumerate(expr):
                if   char == "(": balance += 1
                elif char == ")": balance -= 1
                if balance == 0: return [self._convert(expr[1:idx]), *self._convert(expr[idx+1:])]
        return [expr[0], *self._convert(expr[1:])]


    def parser_out(self, expr: list|str) -> str|None:
        """Convert Python to OPAL syntax."""

        return (
            None if expr is None
            else ("#t" if expr else "#f") if isinstance(expr, bool)
            # else f"'{self.event_parse_expr_out(expr[1])}" if KEY.isquote(expr) 
            else f"({' '.join(self.parser_out(elem) for elem in expr if elem != None)})" if isinstance(expr, list) 
            else str(expr)
        )
