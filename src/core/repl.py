from src.core.opal import opal

from rich.console import Group
from rich.pretty import Pretty
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import print
from rich import box

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


    def interpret(self, expr: str) -> str | Text:
        """Fully interpret a complete expression."""
        
        # Ignore empty lines
        if expr == "": return None
                
        # Identify solitary keywords
        # elif opal.iskeyword(expr): return f"{expr} is an operator, built-in function or reserved word."

        # Match repl-level commands
        elif expr in self.COMMANDS: return self.COMMANDS[expr]()

        # Otherwise parse the line and convert it to Python syntax, evaluate, and return as an ALVIN string 
        return opal.parse_out(opal.evaluate(opal.parse_in(expr)))


    def RER(self, expr: str) -> Message:
        """Read-Evaluate-Return function. Meant to be looped."""
        
        if opal.iscommented(expr):
            # if opal.MULTILINE_COMMENT_CLOSE in expr:
            #     if not expr.startswith(opal.MULTILINE_COMMENT_CLOSE)
            #     else: raise SyntaxError(f"unmatched closing comment in {expr}")
            # elif opal.MULTILINE_COMMENT_OPEN in expr: opal.COMMENT_COUNTER += 1

            return self.Comment()
               
        elif opal.iscomplete(expr):
            try:
                return self.Complete(self.interpret(expr))
            except Exception as e: 
                if opal.dFlag: raise e                
                else: 
                    msg = Text(f"{type(e).__name__}: {e}")
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
            if opal.iFlag: list(self.RERL(stream))
            # Otherwise print banner
            else: print(f"--- {opal} ---")

        # If unsuppressed and interactive, proceed as normal
        elif opal.iFlag:
            print(self.welcome())
            print(self.prompt(), end='')

        for line in self.RERL(stream):
            if line.get() != None: print(line.get())
            if not suppress: print(self.prompt(interim=isinstance(line, self.Incomplete)), end='')



##### Helper Functions #####



    def prompt(self, interim: str = None) -> Text:
        """Returns the interpreter prompt."""
        prompt = f"[{opal.DEFAULT_COLOR}]{" "*(len(opal.PROMPT)-1)}> " if interim else f"[{opal.DEFAULT_COLOR}]{opal.PROMPT}"
        return Text.from_markup(prompt)


    def welcome(self) -> Text:
        """Build a welcome text box."""

        msg = ""

        if opal.iFlag: 
            msg += f"{opal.NAME} v{opal.VERSION}, [{opal.DEFAULT_COLOR}]interactive[/]"

            if opal.dFlag: msg += f" with [cyan]debugging[/cyan]"
        
        msg += "\nEnter 'help' to show further information"

        return Text.from_markup(msg)


    def help(self) -> Panel:
        """Display help information."""

        msg = f"""{opal} is an experimental programming language.
        
Documentation can be found on GitHub:
https://github.com/Antonio-Iijima/ALVIN

{opal.PROMPT}clear     : clear the terminal 
{opal.PROMPT}exit/quit : exit the interpreter
{opal.PROMPT}flags     : display interpreter flags
{opal.PROMPT}keywords  : display all language keywords
{opal.PROMPT}dev.info  : useful development/debugging tools"""
        
        return Group(
            "",
            Panel.fit(
                msg,
                box=box.DOUBLE,
                border_style=opal.DEFAULT_COLOR
            ),
            ""
        )


    def clear(self) -> Text:
        """Clear the terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
        return self.welcome()


    def quit(self) -> None:
        """Exit the interactive interpreter."""

        msg = "Arrivederci!"

        print(
            Group(
                "",
                Panel.fit(
                    msg,
                    box=box.DOUBLE,
                    border_style=opal.DEFAULT_COLOR
                )
            )
        ) or quit()


    def show_closures(self) ->Pretty:
        """Display the current closures."""    
        return Pretty(opal.CLOSURES) if opal.CLOSURES else "No function environments found."
    
              
    def show_globals(self) -> Pretty:
        """Display all global variables."""
        return Pretty(opal.GLOBALS) if opal.GLOBALS else "No global variables found."


    def show_imports(self) -> Pretty:
        """Display all currently imported modules and libraries."""
        return Pretty(opal.IMPORTS) if opal.IMPORTS else "No imported modules found."


    def show_env(self) -> Pretty:
        "Display current environment."
        return Group(
            Pretty(opal.ENV),
            ""
        )


    def show_dev(self) -> Panel:
        """Display useful dev tools."""

        msg = f"""useful tools
                
{opal.PROMPT}dev.closures : closures
{opal.PROMPT}dev.env      : environment
{opal.PROMPT}dev.globals  : global variables
{opal.PROMPT}dev.imports  : imported modules"""
        
        return Group(
            "",
            Panel.fit(
                msg,
                box=box.DOUBLE,
                border_style=opal.DEFAULT_COLOR
            ),
            ""
        )


    def show_keywords(self) -> str|Table:
        """Display all language keywords."""

        if not any(opal.KEYWORDS.values()): return "[red]No keywords found."

        padding = 2

        # Calculate the character limit of each word with padding
        offset = max(max(len(keyword) for keyword in category) for category in opal.KEYWORDS.values() if category) + padding

        title = f"KEYWORDS ({opal.current_keyword_num()}/{opal.INITIAL_KEYWORD_NUM})"
        msg = ""

        categories = { f"{c} ({len(opal.KEYWORDS[c])})" : sorted(opal.KEYWORDS[c]) for c in opal.KEYWORDS}

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
                box=box.DOUBLE,
                border_style=opal.DEFAULT_COLOR,
            ),
            ""
        )
