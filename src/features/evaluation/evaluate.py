def isatom(x): return not isinstance(x, list)
def isnull(x): return x == []


class Evaluate:
    
    def evaluate(self, expr) -> any:
        if isatom(expr): return int(expr)
        
        if isnull(expr): return []

        head, *tail = expr

        if isatom(head):
            
            if head in self.REGULAR:
                return self.REGULAR[head](*map(self.evaluate, tail))
