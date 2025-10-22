"""Strict and latent variable typing."""



from src.lang import interpreter as INT
from src.lang import datatypes as DAT
from src.lang import keywords as KEY



class Variable:

    def __new__(cls, var: str|list, val: any) -> "TypedVariable":
        """Constructs a `Strict` or `Latent` variable object based on the specification of `var` with the value `val`."""
        return Strict(var, val) if isinstance(var, list) else Latent(var, val)



class TypedVariable:

    def __init__(self, var: any, val: any):
        self.name = var
        self.val = val

        self.types = {
            "int"       : KEY.isint,
            "float"     : KEY.isfloat,
            "str"       : KEY.isstring,
            "lazy"      : KEY.islazy,
            "list"      : KEY.islist,
            "frozen"    : KEY.isfrozen,
            "function"  : KEY.isfunction,
            "bool"      : KEY.isbool
        }


    def setVal(self, val: any):
        isinstance(self.val, DAT.Closable) and INT.interpreter.ENV.cleanup(self.name)
        self.val = val

        
    def getVal(self) -> any: return self.val.thaw() if isinstance(self.val, DAT.Frozen) else self.val


    def _getType(self, val) -> str:
        for type, check in self.types.items():
            if check(val): return type


    def __repr__(self): return str(self)



class Strict(TypedVariable):

    def __init__(self, var: list, val: any) -> None:
        super().__init__(var[1], val)
        
        self.type = var[0]
        self.typeCheck()


    def getType(self) -> str: return self.type
        

    def typeCheck(self) -> None:
        """Raises `TypeError` if currently contained variable type is not `self.type`."""
        if not self.types[self.type](self.val): 
            raise TypeError(f"variable {self.name} requires value of type <{self.type}> but received <{self._getType(self.val)}>")


    def setVal(self, val: any) -> "Strict":
        super().setVal(val)
        self.typeCheck()


    def __str__(self) -> str: return f"<strict {self.type} {self.name}>"



class Latent(TypedVariable):
    
    def getType(self):
        return self._getType(self.val)


    def setVal(self, val: any):
        super().setVal(val)
        self.val = val


    def __str__(self) -> str: return f"<latent {self.getType()} {self.name}>"
