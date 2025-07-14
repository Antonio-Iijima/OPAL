"""Custom datatype classes."""



import random

import config as cf
import parser as prs
import evaluate as ev
import keywords as kw
import environment as env



class Closable:
    """Parent class for all OPAL structures supporting closures, i.e. functions and templates (classes)."""

    def __init__(self, name: str, parameters: list = None, body: list = None) -> None:
        """Initialize datatype and generate unique ID."""

        self.name = name
        self.parameters = parameters or []
        self.body = body or []

        # Generate randomized id
        self.id = self.generate_id()

        # Create closed environment
        cf.config.CLOSURES[self.id] = env.Environment()


    def generate_id(self, k: int = 15) -> str: 
        """Generate a randomized identification string between 0 and k digits long."""
        return f"ID:{random.randint(0, 10**k)}.{self.type}.{self.name}"
    

    def __str__(self) -> str: return f"<{self.type} {self.name}>"
    


class Function(Closable):
    """Custom OPAL function class."""

    def __init__(self, name: str, parameters: list = None, body: list = None, isMethod: bool = False) -> None:
        if isMethod:
            self.type = "method"
        elif name == "lambda": 
            self.type = name
        else:
            self.type = "function"

        super().__init__(name, parameters, body)
            
        if self.type == "lambda": self.name = f"{prs.convert(self.parameters)} {prs.convert(self.body)}" 


    def eval(self, args: list) -> any:
        """Function call evaluation."""

        def logic(args: list) -> any:
            """Function evaluation logic."""

            # Match the arguments to the function to its parameters
            cf.config.CLOSURES[self.id].match_arguments(self.parameters, args)

            # Define 'self' as a special local reference to the current function
            self.type in ('lambda', 'self') and cf.config.CLOSURES[self.id].define('self', self.parameters, self.body)

            # Extend the general environment with the current function's closure (i.e. FUNARGs)
            cf.config.ENV.extend(cf.config.CLOSURES[self.id])

            # Evaluate the function
            try:
                value = ev.evaluate(self.body)

                # If returning a function, give it access to current closure
                if isinstance(value, Function): cf.config.CLOSURES[value.id] = cf.config.CLOSURES[self.id].clone()

            # Safely end the extended scopes and remove 'self'
            finally:
                cf.config.ENV.end_scope(len(cf.config.CLOSURES[self.id]))
                self.type in ('lambda', 'self') and cf.config.CLOSURES[self.id].delete('self')

            return value
        
        # Applicative order evaluation for arguments
        args = [] if args == None else kw.evlist(args)

        # Confirm function arity
        if len(self.parameters) != len(args): 
            raise TypeError(f"{self.name} takes {len(self.parameters)} argument{"s"*bool(len(self.parameters)-1)} but {len(args)} were given")
        
        # Execute the actual function logic in local scope
        return cf.config.CLOSURES[self.id].runlocal(logic, args)



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
        cf.config.CLOSURES[self.id].match_arguments(variables.keys(), variables.values())

        # Save template methods to internal environment
        cf.config.CLOSURES[self.id].match_arguments(methods.keys(), methods.values())


    def new(self, args: list) -> "Instance":
        """Create a new template instance."""

        def logic(init: list) -> any:
            """Evaluate all initialization statements."""
            return kw.evlist(init)

        # Instantiate
        newInstance = Instance(self.name, self.parameters, args)

        # Inherit template variables and methods
        cf.config.CLOSURES[newInstance.id].env += cf.config.CLOSURES[self.id].env

        # Run initialization function
        self.init and cf.config.ENV.runClosed(cf.config.CLOSURES[newInstance.id], logic, self.init)
            
        return newInstance
    


class Instance(Closable):
    """Instance of a template."""

    def __init__(self, name: str, parameters: list, args: list) -> None:
        self.type = "instance"

        super().__init__(name, parameters, args)

        # Match parameters to arguments
        cf.config.CLOSURES[self.id].match_arguments(self.parameters, args)
   
    
    def eval(self, method: str, args: list = None):
        """Evaluate call to instance method."""

        def logic(method, args: list):
            """Method evaluation logic."""
            return cf.config.ENV.lookup(method).eval(args)
        
        # Execute logic in local scope
        return cf.config.ENV.runClosed(cf.config.CLOSURES[self.id], logic, method, args)
