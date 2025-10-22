"""Custom datatype classes."""



from src.lang  import interpreter as INT
from src.lang import environment as ENV
from src.lang import evaluate as EVA
from src.lang import keywords as KEY
from src.lang import parser as PAR

import random



class Closable:
    """Parent class for all OPAL structures supporting closures, i.e. functions and templates."""

    def __init__(self, name: str, parameters: list = None, body: list = None) -> None:
        """Initialize datatype and generate unique ID."""

        self.name = name
        self.parameters = parameters or []
        self.body = body or []

        self.id = self.generate_id()

        # Create closed environment
        INT.interpreter.CLOSURES[self.id] = ENV.Environment()


    def generate_id(self, k: int = 15) -> str: 
        """Generate a randomized identification string between 0 and k digits long."""
        return f"ID:{random.randint(0, 10**k)}.{self.type}.{self.name}"
    

    def __str__(self) -> str: return f"<{self.type} {self.name}>"


    def __repr__(self): return str(self)
    


class Function(Closable):
    """Custom OPAL function class."""

    def __init__(self, name: str, parameters: list = None, body: list = None, isMethod: bool = False, isLazy: bool = False) -> None:
        """Initialize closable function type."""

        self.type = "method" if isMethod else "lambda" if name == "lambda" else "function"
        self.isLazy = isLazy

        super().__init__(name, parameters, body)
            
        if self.type == "lambda": self.name = f"{PAR.toOPAL(self.parameters)} {PAR.toOPAL(self.body)}" 


    def eval(self, args: list) -> any:
        """Function call evaluation."""

        def logic(args: list) -> any:
            """Function evaluation logic."""

            # Match the arguments to the function to its parameters
            INT.interpreter.CLOSURES[self.id].match_arguments(self.parameters, args)

            # Define 'self' as a special local reference to the current function
            self.type in ('lambda', 'self') and INT.interpreter.CLOSURES[self.id].define('self', self.parameters, self.body)

            INT.interpreter.ENV.extend(INT.interpreter.CLOSURES[self.id])

            try:
                value = EVA.evaluate(self.body)

                # If returning a function, give it access to current closure
                if isinstance(value, Function): INT.interpreter.CLOSURES[value.id] = INT.interpreter.CLOSURES[self.id].clone()

            finally:
                INT.interpreter.ENV.end_scope(len(INT.interpreter.CLOSURES[self.id]))
                self.type in ('lambda', 'self') and INT.interpreter.CLOSURES[self.id].delete('self')

            return value
        
        # Evaluation of arguments
        args = [] if args == None else args if any(map(KEY.isfrozen, args)) else KEY.evlist(args)
        
        # Confirm function arity
        if len(self.parameters) != len(args): 
            raise TypeError(f"{self.name} takes {len(self.parameters)} argument{"s" if len(self.parameters) > 1 else ""} but {len(args)} {"was" if len(args) == 1 else "were"} given")
             
        # Execute the actual function logic in local scope
        return INT.interpreter.CLOSURES[self.id].runlocal(logic, args)
    


class Template(Closable):
    """Template data type."""

    def __init__(self, name: str, parameters: list = None, body: list = None) -> None:
        self.type = "template"

        super().__init__(name, parameters, body)

        self.init = None

        # Extract template methods and variables        
        methods = { e[1] : Function(*e[1:], isMethod=True) for e in self.body if e[0] == "func" }
        variables = { e[1] : e[2] for e in self.body if e[0] == "var" }

        # Set initialization function if included
        for method in self.body:
            if method[0] == "init":
                self.init = method[1:]
                break

        # Save template variables to internal environment
        INT.interpreter.CLOSURES[self.id].match_arguments(variables.keys(), variables.values())

        # Save template methods to internal environment
        INT.interpreter.CLOSURES[self.id].match_arguments(methods.keys(), methods.values())


    def new(self, args: list) -> "Instance":
        """Create a new template instance."""

        def logic(init: list) -> any:
            """Evaluate all initialization statements."""
            return KEY.evlist(init)

        newInstance = Instance(self.name, self.parameters, args)

        # Inherit template variables and methods
        INT.interpreter.CLOSURES[newInstance.id].env += INT.interpreter.CLOSURES[self.id].env

        self.init and INT.interpreter.ENV.runClosed(INT.interpreter.CLOSURES[newInstance.id], logic, self.init)
            
        return newInstance
    


class Instance(Closable):
    """Instance of a template."""

    def __init__(self, name: str, parameters: list, args: list) -> None:
        self.type = "instance"

        super().__init__(name, parameters, args)

        # Match parameters to arguments
        INT.interpreter.CLOSURES[self.id].match_arguments(self.parameters, args)
   
    
    def eval(self, method: str, args: list = None):
        """Evaluate call to instance method."""

        def logic(method, args: list):
            """Method evaluation logic."""
            return INT.interpreter.ENV.lookup(method).eval(args)
        
        return INT.interpreter.ENV.runClosed(INT.interpreter.CLOSURES[self.id], logic, method, *args)



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



##### Typing #####



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
        isinstance(self.val, Closable) and INT.interpreter.ENV.cleanup(self.name)
        self.val = val

        
    def getVal(self) -> any: return self.val.thaw() if isinstance(self.val, Frozen) else self.val


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
