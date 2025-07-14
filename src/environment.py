"""Environment data structure and all globally accessible structures."""



import copy
import importlib

import config as cf
import evaluate as ev
import datatypes as dt
import extensions as ext



##### Environment #####



class Environment:
    """Environment data structure, represented as a stack of dictionaries."""

    def __init__(self, env: list = None) -> None:
        self.env = env or [{}]


    def clone(self) -> "Environment":
        """Returns a deep copy of the environment."""
        return Environment(copy.deepcopy(self.env))


    def begin_scope(self) -> None:
        """Begin new scope."""
        self.env = [{}] + self.env


    def end_scope(self, n: int = 1) -> None:
        """End n scopes, by default 1."""
        self.env = self.env[n:] if n < len(self.env) else [{}]


    def find_scope(self, var: str, scope: int = 0) -> int:
        """Find and return the index of the lowest scope in which `var` has been declared.
        \nIf not found, return -1."""

        # Searched through entire environment
        if scope == len(self.env): return -1

        # Otherwise look through scopes
        elif var in self.env[scope]: return scope
        else: return self.find_scope(var, scope+1)


    def set(self, var: str, val: any, scope: int = 0) -> None: 
        """Assign `val` to evaluated `var` in an optional scope, by default current."""

        # Garbage collection in case of function
        self.cleanup(var, scope)

        # Evaluate value and assign
        self.env[scope][var] = ev.evaluate(val)


    def define(self, name: str, parameters: list, body: list,) -> None:
        """Define a named function."""
        self.env[0][name] = dt.Function(name, parameters, body)
    
       
    def deftemplate(self, name: str, parameters: list, *body: list,) -> None:
        """Define a new template."""
        self.env[0][name] = dt.Template(name, parameters, body)


    def update(self, var: str, val: any) -> None | str:
        """Reassign previously declared `var` to new `val`."""

        # Locate variable
        scope = self.find_scope(var)

        # If variable not found
        if scope == -1: raise NameError(f"cannot update variable '{var}' before assignment.")

        # Otherwise reassign
        else: self.set(var, val, scope)


    def delete(self, var: str, scope=0) -> None | str: 
        """Delete lowest declaration of `var` or raise `NameError`."""

        # Locate variable
        scope = self.find_scope(var)

        # If variable not found
        if scope == -1: raise NameError(f"cannot delete variable '{var}' before assignment.")

        # Garbage collection in case of function
        self.cleanup(var, scope)

        # And remove
        self.env[scope].pop(var)


    def delex(self, extension: str) -> None:
        """Delete an extension."""

        # Validate that extension exists
        valid = extension in cf.config.EXTENSIONS

        if valid:

            # Bookend indices
            start = end = 0

            for i, (name, idx) in enumerate(cf.config.EXTENSION_INDEX):
                end += idx
                if name == extension: 
                    
                    # Remove entry from index
                    cf.config.EXTENSION_INDEX.pop(i); break
                start += idx

            # Get the current contents of the extensions.py file
            contents = open(f"{cf.config.PATH}/src/extensions.py").readlines()
            
            # Excise selected extension
            contents = contents[:start] + contents[end:]    
            
            # Rewrite extensions.py
            with open(f"{cf.config.PATH}/src/extensions.py", "w") as file:
                file.writelines(contents)
                
            # Reload extensions to make changes visible
            importlib.reload(ext)

            # Remove entry from log
            cf.config.EXTENSION_LOG.remove(extension)

            # Remove entry from keywords
            cf.config.EXTENSIONS.pop(extension)
            cf.config.KEYWORDS.remove(extension)

        else: raise NameError(f"extension '{extension}' not found.")


    def match_arguments(self, parameters: list, args: list) -> None:
        """Matches a list of parameters with a list of arguments for use in functions."""
        for var, val in zip(parameters, args): self.env[0][var] = val


    def lookup(self, var: str, scope: int = 0) -> any:
        """Finds nearest declaration of `var`."""

        # Locate variable
        scope = self.find_scope(var)

        # If variable not found
        if scope == -1: 

            # Check if it is the name of an imported module
            if var in cf.config.IMPORTS: print(f"'{var}'{"" if cf.config.IMPORTS[var].__name__ == var else f" (or {cf.config.IMPORTS[var].__name__})"} is an imported module.")

            # Otherwise raise error
            else: raise ValueError(f"variable {var} is not defined.")

        # Otherwise return value
        else: return self.env[scope][var]


    def runlocal(self, logic: callable, *args) -> any:
        """Run any function in a local scope which is destroyed when the function returns."""

        # Begin a new local scope
        self.begin_scope()

        # Evaluate the provided procedure logic
        try:
            value = logic(*args)

        # Ensure local scope is always ended
        finally: 
            self.end_scope()

        return value


    def runClosed(self, closure: "Environment", logic: callable, *args) -> any:
        """Extended version of the runLocal method which allows for the closure of a function."""

        # Extend the general environment
        self.extend(closure)
        self.begin_scope()

        # Evaluate the passed function
        try:
            value = logic(*args)

        # Safely end the extended scopes
        finally:
            closure.env = self.env[:len(closure)+1]
            self.end_scope(len(closure))

        return value


    def extend(self, other: "Environment") -> None:
        """Add another environment as lowest scope to current environment."""
        self.env = other.env + self.env


    def cleanup(self, var: str, scope: int = 0) -> None:
        """Basic garbage collection for the closure environments attached to functions."""

        # Get the current variable; if it is a closable, remove its closure
        current = self.env[scope].get(var, None); isinstance(current, dt.Closable) and cf.config.CLOSURES.pop(current.id) 


    def __len__(self) -> int: return len(self.env)


    def __str__(self) -> str:
        """Properly organize the Environment for printing."""

        display = ""
        for scope, contents in enumerate(self.env):
            display += f"\nScope {scope}\n"
            for var, val in contents.items():
                display += f"\n {var} : {val}"
            display += "\n"
        
        return display
