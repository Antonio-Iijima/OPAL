"""Read, Eval, Print, Loop."""



import sys

import config as cf
import parser as prs
import keywords as kw
import evaluate as ev
import interpreter as intrp



##### REPL / Command-Line #####



def REPL(stream: str = sys.stdin, loadingFile: bool = False) -> None:
    """Process a stream or load a file."""
    
    # Selectively display prompts/interactions
    showContent = cf.config.iFlag and not loadingFile

    if cf.config.iFlag:
        if not loadingFile: 
            intrp.interpreter.welcome()
            intrp.interpreter.prompt()
    else: print(f"--- OPAL v{cf.config.VERSION} ---")
        
    expression = ""

    for line in stream:

        # Handle commented lines
        if prs.iscomment(line):
            if cf.config.MULTILINE_COMMENT_CLOSE in line:
                if cf.config.COMMENT_COUNTER: cf.config.COMMENT_COUNTER -= 1
                else: raise SyntaxError(f"unmatched closing comment in {line}")
            elif cf.config.MULTILINE_COMMENT_OPEN in line: cf.config.COMMENT_COUNTER += 1
            continue        
        
        # Otherwise continue building expression
        expression += f"{line}\n" if loadingFile else line

        # If the expression is probably complete
        if prs.iscomplete(expression):
            
            try: run(expression, loadingFile)

            except Exception as e:

                if cf.config.dFlag:
                    
                    # Safely exit extensions and raise full error
                    intrp.interpreter.exit_extensions(); raise e
                
                else:

                    # Just print exception without breaking the REPL
                    print(f"{type(e).__name__}: {e}")
                    
                    # Random keyword deletion mode, because why not?
                    if cf.config.zFlag: intrp.interpreter.del_random_keyword()
            
            #  Print the prompt again and reset the expression
            if showContent: intrp.interpreter.prompt()

            expression = ""

        # Otherwise print the 'interim' prompt for multiline expressions
        elif showContent: intrp.interpreter.prompt(interim=True)

    # If we get ot the end of the stream without seeing the quit() command (e.g. when loading a file)
    else:
        if not cf.config.iFlag: intrp.interpreter.exit_extensions()



##### Helper Functions #####



def run(line: str, loadingFile: bool = False) -> None:
    """Execute a complete expression and print output, if any."""

    output = interpret(line.strip())

    # If the output is None, the line probably has its own output solution
    if output is not None and cf.config.iFlag != loadingFile: print(output)


def interpret(line: str) -> any:
    """Fully interpret a complete expression."""
    
    # Ignore empty lines
    if line == "": return None
    
    # Interpret using the Python interpreter
    elif line.startswith("python"): print(eval(line.removeprefix("python")))

    # Handle language extensions
    elif line.startswith("@start"): intrp.interpreter.extend(line)
    
    # Identify solitary keywords
    elif kw.iskeyword(line): print(f"{line} is an operator, built-in function or reserved word.")

    # Match interpreter commands
    elif line in intrp.interpreter.INTERPRETER: intrp.interpreter.INTERPRETER[line]()

    # Otherwise parse the line and convert it to Python syntax, evaluate, and return as an OPAL string 
    else: return prs.toOPAL(ev.evaluate(prs.parse(line)))
