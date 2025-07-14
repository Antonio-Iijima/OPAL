"""Main program to run the OPAL interpreter."""



import sys

import repl as rpl
import config as cf
import interpreter as intrp



##### Setup & Main Program #####



def main(args: list = sys.argv) -> None:
    """Main program."""

    # Because implementing a language in Python is really inefficient
    sys.setrecursionlimit(10**5)

    # Setup config with flags
    cf.config.initialize({
        '-i' : '-i' in sys.argv, # interactive interpreter
        '-d' : '-d' in sys.argv, # debugging
        '-p' : '-p' in sys.argv, # permanent extension changes
        '-z' : '-z' in sys.argv, # why
    })

    # Remove flags from args
    for flag in cf.config.FLAGS: flag in args and args.remove(flag)
    
    # If called with nothing else, print the version and exit
    if not (args[1:] or cf.config.iFlag): intrp.interpreter.prompt(); print(f"OPAL Programming Language version {cf.config.VERSION}"); exit()

    # Read in files if necessary
    for item in args[1:]:
        with open(item, "r") as file:
            rpl.REPL(file.read().splitlines(), True)

    # Start interactive session
    if cf.config.iFlag:
        try: rpl.REPL()

        # Catch exiting exceptions and safely quit extensions
        except BaseException as e: 
            intrp.interpreter.exit_extensions(); print()
            
            # Don't print ctrl-c because I use it more than quit; only raise other unexpected errors
            if type(e) != KeyboardInterrupt: raise e



if __name__ == "__main__": main()
