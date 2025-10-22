"""Environment data structure and all globally accessible structures."""



from src.lang  import interpreter as INT
from src.lang import datatypes as DAT

import copy



##### Environment #####



class Environment:
    """Environment data structure, represented as a stack of dictionaries."""

    def __init__(self, env: list = None) -> None:
        self.env = env or [{}]


    ### Scope Management ###


    def clone(self) -> "Environment":
        """Returns a deep copy of the environment."""
        return Environment(copy.deepcopy(self.env))


    def begin_scope(self) -> None:
        """Begin new scope."""
        self.env = [{}] + self.env


    def end_scope(self, n: int = 1) -> None:
        """End n scopes, by default 1."""
        self.env = self.env[n:] if n < len(self.env) else [{}]


    def extend(self, other: "Environment") -> None:
        """Add another environment as lowest scope to current environment."""
        self.env = other.env + self.env


    def runlocal(self, logic: callable, *args) -> any:
        """Run any function in a local scope which is destroyed when the function returns."""

        self.begin_scope()

        try:
            value = logic(*args)
        finally: 
            self.end_scope()

        return value


    def runClosed(self, closure: "Environment", logic: callable, *args) -> any:
        """Extended version of the runLocal method which allows for the closure of a function."""

        self.extend(closure)
        self.begin_scope()

        try:
            value = logic(*args)
        finally:
            closure.env = self.env[:len(closure)+1]
            self.end_scope(len(closure))

        return value


    ### Variable Management ###


    def find_scope(self, var: str|list, scope: int = 0) -> int|None:
        """Find and return the index of the lowest scope in which `var` has been declared. If not found, return None."""
        
        return (
            None if scope == len(self.env)
            else scope if var in self.env[scope]
            else self.find_scope(var, scope+1)
        )


    def lookup(self, var: str, scope: int = 0) -> any:
        """Finds nearest declaration of `var`."""

        scope = self.find_scope(var)

        if scope is None: 
            if var in INT.interpreter.IMPORTS: print(f"'{var}'{"" if INT.interpreter.IMPORTS[var].__name__ == var else f" (or {INT.interpreter.IMPORTS[var].__name__})"} is an imported module.")
            else: raise NameError(f"variable {var} is not defined.")
        else: 
#            print(f"LOOKUP: {var}")
#            print(f"FOUND: {self.env[scope][var].getVal()}")
            return self.env[scope][var].getVal()
            

    def cleanup(self, var: str, scope: int = 0) -> None:
        """Basic garbage collection for the closure environments attached to functions."""

        # Get the current variable; if it is a closable, remove its closure
        current = self.env[scope][var].getVal(); isinstance(current, DAT.Closable) and INT.interpreter.CLOSURES.pop(current.id) 


    def set(self, var: str, val: any, scope: int = None) -> None: 
        """Assign `val` to `var` in an optional scope, by default current."""

        name = var[1] if isinstance(var, list) else var
        scope = scope or 0

        # Set currentVar
        currentVar = self.env[scope].get(name)

        # Variable is either `Strict`, or `Latent`/undeclared
        if isinstance(currentVar, DAT.Strict): currentVar.setVal(val)
        else: self.env[scope][name] = DAT.Variable(var, val)


    def delete(self, var: str) -> None | str: 
        """Delete lowest declaration of `var` or raise `NameError`."""

        scope = self.find_scope(var)

        if scope is None: raise NameError(f"cannot delete variable '{var}' before assignment.")

        self.cleanup(var, scope)
        self.env[scope].pop(var)


    def define(self, name: str, parameters: list, body: list,) -> None:
        """Define a named function."""
        self.set(name, DAT.Function(name, parameters, body))
       

    def deftemplate(self, name: str, parameters: list, *body: list,) -> None:
        """Define a new template."""
        self.set(name, DAT.Template(name, parameters, body))


    def match_arguments(self, parameters: list, args: list) -> None:
        """Matches a list of parameters with a list of arguments for use in functions."""
        for var, val in zip(parameters, args): self.set(var, val)


    ### Other Methods ###


    def __len__(self) -> int: return len(self.env)


    def __str__(self) -> str:
        """Properly organize the Environment for printing."""

        display = ""
        for scope, contents in enumerate(self.env):
            display += f"\nScope {scope}\n"
            for var, val in contents.items():
                display += f"\n {var} : {val}"
            display += "\n" if contents.items() else "\nNone\n "
        
        return display


    def __repr__(self): return str(self)
