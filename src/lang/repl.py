"""Read, Eval, Print, Loop."""



from src.lang import interpreter as INT
from src.lang import evaluate as EVA
from src.lang import keywords as KEY
from src.lang import parser as PAR

from rich.console import Group
from rich.pretty import Pretty
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import print

import os
import sys



##### REPL / Command-Line #####



class REPL:

    def __init__(self):

        self.COMMANDS = {
            "help"          : self.help,
            "keywords"      : self.show_keywords,
            "exit"          : self.quit,
            "quit"          : self.quit,
            "flags"         : self.flags,
            "clear"         : self.clear,
            "dev.info"      : self.show_dev,
            "dev.closures"  : self.show_closures,
            "dev.globals"   : self.show_globals,
            "dev.imports"   : self.show_imports,
            "dev.env"       : self.show_env
        }
        "Internal REPL commands"


    class Message:
        """Base class for internal REPL messages."""

        def __init__(self, msg: any = None): self.msg = msg
        
        def get(self) -> any: return self.msg

    class Comment(Message): 
        """Expression is commented."""

    class Complete(Message):
        """Expression is complete and evaluated."""

    class Incomplete(Message):
        """Expression is incomplete."""

    class Error(Message):
        """Error in evaluating expression."""


    def RER(self, expr) -> Comment|Complete|Incomplete|Error:
        """Read-Evaluate-Return function. Meant to be looped."""
        
        if PAR.iscommented(expr):
            if INT.interpreter.MULTILINE_COMMENT_CLOSE in expr:
                if INT.interpreter.COMMENT_COUNTER: INT.interpreter.COMMENT_COUNTER -= 1
                else: raise SyntaxError(f"unmatched closing comment in {expr}")
            elif INT.interpreter.MULTILINE_COMMENT_OPEN in expr: INT.interpreter.COMMENT_COUNTER += 1

            return self.Comment()
               
        elif PAR.iscomplete(expr):
            try:
                return self.Complete(self.interpret(expr))
            except Exception as e: 
                if INT.interpreter.dFlag: raise e                
                else: 
                    msg = Text(f"{type(e).__name__}: {e}")
                    if INT.interpreter.zFlag: msg.append_text(INT.interpreter.del_random_keyword())
            
                    return self.Error(msg)
                                    
        return self.Incomplete()
            

    def RERL(self, stream: str = sys.stdin):
        """Read-Evaluate-Return-Loop. Wrapper for `RER`. Yields a continuous stream of output (generator)."""

        expr = ""

        for line in stream:

            expr += f"{line}\n"

            output = self.RER(expr.strip())

            # Reset expression during comments and on completion/error
            if not isinstance(output, self.Incomplete): expr = ""
            if not isinstance(output, self.Comment): yield output


    def REPL(self, stream = sys.stdin, suppress = False) -> None:
        """Read-Evaluate-Print-Loop. Converts `RERL` output to interactive stdout."""

        # Suppress prompts if reading from file 
        if suppress: 

            # Completely silent if continuing into interactive shell
            if INT.interpreter.iFlag: list(self.RERL(stream))
            # Otherwise print banner
            else: print(f"--- OPAL v{INT.interpreter.VERSION} ---")

        # If unsuppressed and interactive, proceed as normal
        elif INT.interpreter.iFlag:
            print(self.welcome())
            print(self.prompt(), end='')

        for line in self.RERL(stream):
            if line.get() != None: print(line.get())
            if not suppress: print(self.prompt(interim=isinstance(line, self.Incomplete)), end='')


    def interpret(self, expr: str) -> str | Text:
        """Fully interpret a complete expression."""
        
        # Ignore empty lines
        if expr == "": return None
        
        # Interpret using the Python interpreter
        elif expr.startswith("python"): return f"{eval(expr.removeprefix("python"))}"
        
        # Handle language extensions
        elif expr.startswith("@start"): return INT.interpreter.extend(expr)
        
        # Identify solitary keywords
        elif KEY.iskeyword(expr): return f"{expr} is an operator, built-in function or reserved word."

        # Match repl-level commands
        elif expr in self.COMMANDS: return self.COMMANDS[expr]()

        # Otherwise parse the line and convert it to Python syntax, evaluate, and return as an OPAL string 
        return PAR.toOPAL(EVA.evaluate(PAR.parse(expr)))



##### Helper Functions #####



    def prompt(self, interim: str = None) -> Text:
        """Returns the interpreter prompt."""
        prompt = f"[{INT.interpreter.DEFAULT_COLOR}]{" "*(len(INT.interpreter.PROMPT_SYMBOL)-1)}> " if interim else INT.interpreter.PROMPT
        return Text.from_markup(prompt)


    def welcome(self) -> Text:
        """Build a welcome text box."""

        msg = ""

        if INT.interpreter.iFlag: 
            msg += f"OPAL v{INT.interpreter.VERSION}, [green]interactive[/green]"

            if INT.interpreter.dFlag: msg += f" with [cyan]debugging[/cyan]"
        
        if INT.interpreter.pFlag: msg += f"\n[yellow]Permanent extensions enabled[/yellow]"

        msg += "\nEnter 'help' to show further information"

        if INT.interpreter.zFlag: msg += f"\n[red]WARNING: Random keyword deletion enabled. [purple]Proceed at your own risk."

        return Text.from_markup(msg)


    def help(self) -> Panel:
        """Display help information."""

        msg = f"""OPAL is a multi-paradigm experimental programming language based on the previous Alvin Programming Language.
        
Documentation can be found on GitHub:
https://github.com/Antonio-Iijima/OPAL

{INT.interpreter.PROMPT}clear     : clear the terminal 
{INT.interpreter.PROMPT}exit/quit : exit the interpreter
{INT.interpreter.PROMPT}python *. : evaluate *. using Python
{INT.interpreter.PROMPT}flags     : display interpreter flags
{INT.interpreter.PROMPT}keywords  : display all language keywords
{INT.interpreter.PROMPT}dev.info  : useful development/debugging tools"""
        
        return Group(
            "",
            Panel.fit(
                msg,
                box=INT.interpreter.DEFAULT_OUTLINE,
                border_style=INT.interpreter.DEFAULT_COLOR
            ),
            ""
        )


    def clear(self) -> Text:
        """Clear the terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
        return self.welcome()


    def quit(self) -> None:
        """Exit the interactive interpreter."""

        INT.interpreter.exit_extensions()

        msg = ""

        if INT.interpreter.zFlag:
            net = INT.interpreter.current_keyword_num() - INT.interpreter.INITIAL_KEYWORD_NUM
            msg = f"\n[purple]You made {INT.interpreter.ERROR_COUNTER} error{"s" if INT.interpreter.ERROR_COUNTER != 1 else ""} with a net change of {f"+{net}" if net > 0 else net} function{"s" if abs(net)!=1 else ""}\n" + msg

        print(
            Group(
                msg,
                Panel.fit(
                    "Arrivederci!",
                    box=INT.interpreter.DEFAULT_OUTLINE,
                    border_style=INT.interpreter.DEFAULT_COLOR
                ),
                ""
            )
        ) or quit()


    def flags(self) -> Panel:
        """Display current active and inactive flags."""

        msg = "\n".join(f"{flag} : {int(INT.interpreter.FLAGS[flag])}" for flag in INT.interpreter.FLAGS)

        return Group(
            "",
            Panel.fit(
                msg,
                title="Flags",
                box=INT.interpreter.DEFAULT_OUTLINE,
                border_style=INT.interpreter.DEFAULT_COLOR,
                highlight=True
            ),
            ""
        )


    def show_closures(self) ->Pretty:
        """Display the current closures."""    
        return Pretty(INT.interpreter.CLOSURES) if INT.interpreter.CLOSURES else "No function environments found."
    
              
    def show_globals(self) -> Pretty:
        """Display all global variables."""
        return Pretty(INT.interpreter.GLOBALS) if INT.interpreter.GLOBALS else "No global variables found."


    def show_imports(self) -> Pretty:
        """Display all currently imported modules and libraries."""
        return Pretty(INT.interpreter.IMPORTS) if INT.interpreter.IMPORTS else "No imported modules found."


    def show_env(self) -> Pretty:
        "Display current environment."
        return Group(
            Pretty(INT.interpreter.ENV),
            ""
        )


    def show_dev(self) -> Panel:
        """Display useful dev tools."""

        msg = f"""useful tools
                
{INT.interpreter.PROMPT}dev.closures : closures
{INT.interpreter.PROMPT}dev.env      : environment
{INT.interpreter.PROMPT}dev.globals  : global variables
{INT.interpreter.PROMPT}dev.imports  : imported modules"""
        
        return Group(
            "",
            Panel.fit(
                msg,
                box=INT.interpreter.DEFAULT_OUTLINE,
                border_style=INT.interpreter.DEFAULT_COLOR
            ),
            ""
        )


    def show_keywords(self) -> str|Table:
        """Display all language keywords."""

        if not any(INT.interpreter.KEYWORDS.values()): return "[red]No keywords found."

        padding = 2

        # Calculate the character limit of each word with padding
        offset = max(max(len(keyword) for keyword in category) for category in INT.interpreter.KEYWORDS.values() if category) + padding

        title = f"KEYWORDS ({INT.interpreter.current_keyword_num()}/{INT.interpreter.INITIAL_KEYWORD_NUM})"
        msg = ""

        categories = { f"{c} ({len(INT.interpreter.KEYWORDS[c])})" : sorted(INT.interpreter.KEYWORDS[c]) for c in INT.interpreter.KEYWORDS}

        for section_idx, section_title in enumerate(categories):

            # Add spacing between categories
            if section_idx > 0: msg += "\n\n"

            # Add the section title
            msg += f"{" "*((offset*3-len(section_title))//2)}{section_title}\n"

            # Iterate through the keywords in the section to organize into columns
            for keyword_idx, keyword in enumerate(categories[section_title]):

                # Move to the next row every three keywords
                if keyword_idx % 3 == 0: msg += f"\n{" " * padding}"

                # Add each keyword along with the necessary amount of whitespace to justify the columns
                msg += f"{keyword}{' ' * (offset-len(keyword))}"

                # If it is the end of a section and the keywords need to be justified
                column = (keyword_idx + 1) % 3
                if keyword_idx == len(categories[section_title]) - 1 and column != 0:
                    # Replace the 'missing words' with whitespace to complete the columns
                    msg += ' ' * offset * (2 if column == 1 else 1)
        
        return Group(
            "",
            Panel.fit(
                msg,
                title=title,    
                box=INT.interpreter.DEFAULT_OUTLINE,
                border_style=INT.interpreter.DEFAULT_COLOR,
            ),
            ""
        )
