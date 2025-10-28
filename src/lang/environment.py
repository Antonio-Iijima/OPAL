"""
## The Environment

The Environment is possibly the most essential part of any programming language implementation.
OPAL is no different in this respect. The Environment is defined as a class, and serves two main
purposes:

- Variable and function definition
- Scope management

The Environment is instantiated as a class variable of the `Interpreter`. Explicit usage involves
calling it through `evaluate()` with `set` or `def`. More complex internal control over the Environment
is necessary for many other structures (closed functions and `let` statements); this is handled internally
by calling `Environment` methods directly.

---
"""



from src.lang import interpreter as INT
from src.lang import datatypes as DAT

import copy



##### Environment #####



class Environment:
    """Environment data structure, represented as a stack of dictionaries."""


    def __init__(self, env: list[dict] = None) -> None:
        self.env = env or [{}] # Potentially reimplement as deque


    ### Scope Management ###


    def clone(self) -> "Environment":
        """Makes a deep copy of the environment. Used by functions to safely inherit parent closures.
        
        :return: A new `Environment` instance containing a deep copy of the current `env`."""

        return Environment(copy.deepcopy(self.env))


    def begin_scope(self) -> None:
        """Begin new scope.
            
            (burrow)
        
        `burrow` should be used in code only with extreme caution.
        """
        
        self.env = [{}] + self.env


    def end_scope(self, n: int = 1) -> None:
        """Destroy $n$ scopes, by default 1.
        
            (surface)

        `surface` removes one scope only. Should be used in code only with extreme caution. 

        :param `int` n: The number of scopes to clear."""

        self.env = self.env[n:] if n < len(self.env) else [{}]


    def extend(self, other: "Environment") -> None:
        """Extend the current `Environment` with the `env` of another `Environment`. New `env`
        is added as lowest scope to current `Environment`.
        
        :param `Environment` other: Another `Environment` instance."""
        
        self.env = other.env + self.env


    def runlocal(self, logic: callable, *args, **kwargs) -> any:
        """Run any function in a local scope, which is destroyed when the function returns.
        
        :param `callable` logic: The internal logic of the function to be run locally.
        :param `*` args: Positional arguments to be passed to `logic`. 
        :param `**` kwargs: Keyword arguments to be passed to `logic`.
        
        :return: The output of `logic(*args, **kwargs)` in local scope."""

        self.begin_scope()

        try:
            value = logic(*args, **kwargs)
        finally: 
            self.end_scope()

        return value


    def runClosed(self, closure: "Environment", logic: callable, *args, **kwargs) -> any:
        """Extended version of the `runLocal` method which allows for the closure of a function.
        
        :param `Environment` closure: A closure `Environment`, should be from `INT.interpreter.CLOSURES`.
        :param `callable` logic: The internal logic of the function to be run locally.
        :param `*` args: Positional arguments to be passed to `logic`. 
        :param `**` kwargs: Keyword arguments to be passed to `logic`.
        
        :return: The output of `logic(*args, **kwargs)` in local enclosed scope."""

        self.extend(closure)
        self.begin_scope()

        try:
            value = logic(*args, **kwargs)
        finally:
            closure.env = self.env[:len(closure)+1]
            self.end_scope(len(closure))

        return value


    ### Variable Management ###


    def find_scope(self, var: str, scope: int = None) -> int|None:
        """Finds the index of the lowest scope in which `var` has been declared.
        
        :param `str` var: Variable name to be searched.
        :param (optional) `int` scope: If provided, begins search at given scope. Otherwise starts from lowest scope.
        
        :return: The scope of the variable, or `None` if has not been declared."""
        
        scope = scope or 0

        return (
            None if scope == len(self.env)
            else scope if var in self.env[scope]
            else self.find_scope(var, scope+1)
        )


    def lookup(self, var: str) -> any:
        """Looks up the value of a declared variable.
        
        :param `str` var: Variable name to be looked up.
        
        :return: The value of the variable if declared.
        
        :raises: `NameError` if variable is not declared."""

        scope = self.find_scope(var)

        if scope is None: 
            if var in INT.interpreter.IMPORTS: 
                print(f"'{var}'{"" if INT.interpreter.IMPORTS[var].__name__ == var\
                else f" (or {INT.interpreter.IMPORTS[var].__name__})"} is an imported module.")
            else: raise NameError(f"variable {var} is not defined.")
        else: 
            return self.env[scope][var].getVal()
            

    def cleanup(self, var: str, scope: int = None) -> None:
        """Basic garbage collection for the closure environments attached to functions.

        When a function or other `Closable` object is removed from the environment, its closure
        `Environment` persists independently as an entry in `INT.interpreter.CLOSURES` and must be
        manually removed. `cleanup()` is therefore run whenever a variable is removed from the `Environment`, 
        to check if it is a `Closable`; if so, it removes its entry.
        
        :param `str` var: The variable name to be checked.
        :param (optional) `int` scope: If provided, begins search at given scope. Otherwise starts from lowest scope."""

        scope = scope or 0

        # Get the current variable; if it is a closable, remove its closure
        current = self.env[scope][var].getVal(); isinstance(current, DAT.Closable) and INT.interpreter.CLOSURES.pop(current.id) 


    def set(self, var: list|str, val: any, scope: int = None) -> None: 
        """Assign a value to a variable.

            (set a 1)
            (set (float b) 3.14)
        
        The core function of the `Environment`, nearly every operation in the language involves this method
        to some degree. `set()` takes a variable declaration and creates a `Latent` or `Strict` variable object
        containing the provided value. A few points to note:
        
        - In previous implementations, `set()` would evaluate automatically`val` before binding. This has been
        deprecated in favor of the increased flexibility of allowing caller to choose whether and how to evaluate.
            - The built-in function `set` (e.g. `(set a 1)`) **does** evaluate `val`.
        - `Strict` objects are only created if a type is specified in the passed `var`, i.e. `(int a)`. Otherwise
        `Latent` objects are the default.
        - In keeping with the first point, **`set()` does not look up the passed variable**. If the caller wants
        `set()` to update a previously declared variable (if it exists), the output of `Environment.find_scope(var)` 
        should be explicitly passed to `scope`. This will then be used if the variable exists, else lowest scope.
        
        :param `list|str` var: The variable name. If passed a list, the first element must be a type and the 
        second must be the variable name. The variable object will be `Strict` with the type set to that provided.
        Otherwise, the variable will be `Latent` and the type determined by the bound value.
        :param `any` val: A value to be bound to the variable."""

        scope = scope or 0
        name = var[1] if isinstance(var, list) else var

        # Set currentVar
        currentVar = self.env[scope].get(name)

        # Variable is either `Strict`, or `Latent`/undeclared
        if isinstance(currentVar, DAT.Strict): currentVar.setVal(val)
        else: self.env[scope][name] = DAT.Variable(var, val)


    def delete(self, var: str) -> None | str: 
        """Deletes a declared variable.
        
            (del x)

        :param `str` var: The name of the variable to be deleted.
        
        :raises: `NameError` if variable is not declared."""

        scope = self.find_scope(var)

        if scope is None: raise NameError(f"cannot delete variable '{var}' before assignment.")

        self.cleanup(var, scope)
        self.env[scope].pop(var)


    def define(self, name: str, parameters: list, body: list) -> None:
        """Define a named function.

            (def f (x y) (+ x y))
            (def g ((int x) y) (+ x y))
        
        This is essentially a wrapper for `set()` which builds a `Function` object from the provided
        arguments, and passes that to `set()`'s `val` parameter.
        
        :param `str` name: The name of the function.
        :param `list` parameters: The parameters of the function. Each parameter can be either `Latent`
        (no type included, variable name only) or `Strict` (type included in a tuple with the variable name).
        :param `list` body: The function body to be evaluated on call."""

        self.set(name, DAT.Function(name, parameters, body))
       

    def deftemplate(self, name: str, parameters: list, *body: list,) -> None:
        """Define a new template."""
        self.set(name, DAT.Template(name, parameters, body))


    def match_arguments(self, parameters: list, args: list) -> None:
        """Matches a list of parameters with a list of arguments. Primarily for use in functions.
        
        :param `list` parameters: A list of parameters (variable names).
        :param `list` args: A list of arguments to be bound to the parameters."""
        
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
