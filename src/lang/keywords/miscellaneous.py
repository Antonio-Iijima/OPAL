"""Other miscellaneous functions."""



from src.lang  import interpreter as INT
from src.lang import evaluate as EVA
from src.lang import repl as REP

import importlib



def OPAL_eval(expr: any) -> any:
    """Interpreter access from the command line for quoted expressions."""
    return EVA.evaluate(expr[1])


def getfile(filepath: str) -> list:
    """File system access."""
    return open(filepath).readlines()


def import_lib(name: str, _as: str = None, alias: str = None) -> None:
    """Import a library with an optional alias."""

    alias = alias or name
    name = importlib.import_module(name)
    INT.interpreter.IMPORTS[alias] = name


def load(location: str) -> None:
    """Load and run a .op file from provided relative location."""

    # Require .op files for reliability
    if not location.endswith(".op"): raise IOError(f"ensure file extension is *.op.")
    
    with open(location, "r") as file: REP.REPL(file.read().split("\n"), True)


def run_method(imported: str, args: list) -> any:
    """Call a method from an imported module or library."""

    module, method = imported.split(".")

    # Use the module and method strings to get the callable function
    imported = getattr(INT.interpreter.IMPORTS[module], method)

    # Either call the function with arguments or return it if none are provided
    return imported(*args) if callable(imported) else imported


def globals(var: str, val: any = None) -> None:
    """Define or access global variables."""

    # If val is provided, evaluate and assign it to var in the GLOBALS dictionary
    if val: INT.interpreter.GLOBALS[var] = EVA.evaluate(val)

    # Otherwise look up and return the value of var if it exists
    else: return INT.interpreter.GLOBALS.get(var, ValueError)
