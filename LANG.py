"""Main program to run the OPAL interpreter."""



from src.lang import interpreter as INT
from src.lang import repl as REP

from rich.traceback import install
from rich import print

import fileinput
import sys



##### Setup & Main Program #####



if __name__ == "__main__":
    
    # Pretty tracebacks
    install(show_locals=True)

    # Because implementing a language in Python is really inefficient
    sys.setrecursionlimit(10**5)

    # Setup interpreter with flags
    INT.interpreter = INT.Interpreter(
        flags = {
        '-i' : '-i' in sys.argv, # interactive interpreter
        '-d' : '-d' in sys.argv, # debugging
        '-p' : '-p' in sys.argv, # permanent extension changes; not typically recommended
        '-z' : '-z' in sys.argv, # why
    })

    REPL = REP.REPL()

    # Remove flags from args
    for flag in INT.interpreter.FLAGS: flag in sys.argv and sys.argv.remove(flag)
    
    # If called with nothing else, print the version and exit
    if not (sys.argv[1:] or INT.interpreter.iFlag): print(REPL.prompt(), end=''); print(f"OPAL Programming Language version {INT.interpreter.VERSION}"); exit()

    try:
        # Read in files if necessary
        if sys.argv[1:]: REPL.REPL(fileinput.input(), suppress=True)

        # Start interactive session
        if INT.interpreter.iFlag:
            REPL.REPL()

    # Ignore ctrl-c because I use it more than quit; only raise other unexpected errors
    except KeyboardInterrupt: print()

    # Always safely quit extensions
    finally: INT.interpreter.exit_extensions()
