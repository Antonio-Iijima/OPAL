"""Lazy evaluation."""



from src.lang import evaluate as EVA



class Lazy:
    def __init__(self, func: str):
        self.func = func


    def eval(self, args: list) -> any: return EVA.evaluate([self.func, *map(Frozen, args)])


    def __str__(self) -> str: return f"<{self.__class__.__name__.lower()} {self.func}>"


    def __repr__(self): return str(self)



class Frozen:
    def __init__(self, val: str) -> None:
        self.value = val


    def thaw(self):
        """Compute the value of a `Frozen` expression."""
        return EVA.evaluate(self.value)
    

    def __str__(self): return f"<frozen {self.value}>"


    def __repr__(self): return str(self)
