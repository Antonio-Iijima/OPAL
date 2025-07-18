"""Manage interaction with the interpreter command-line."""



import os
import math
import random
import importlib

import config as cf
import extensions as ext



class Interpreter():
    """Interpreter command-line management."""

    def __init__(self):
        """Initialize exposed commands."""

        self.INTERPRETER = {
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


    def prompt(self, interim=False) -> None:
        """Prints the interpreter prompt."""
        text = cf.config.set_color(" "*(len(cf.config.PROMPT_SYMBOL)-2) + "> ") if interim else cf.config.PROMPT; print(text, flush=True, end='')


    def welcome(self) -> None:
        """Display a welcome text box."""

        display = """Welcome to OPAL
Omni-Paradigm Language"""

        self.text_box(display, centered=True)

        cf.config.iFlag and print(f"OPAL v{cf.config.VERSION}, interactive mode", end='\n'*(not cf.config.dFlag))
        cf.config.dFlag and print(" with debugging")
        cf.config.pFlag and print("Permanent extensions enabled")

        print("Enter 'help' to show further information")

        cf.config.zFlag and print(f"{cf.config.COLORS["red"]}WARNING: Random keyword deletion enabled.{cf.config.COLORS["purple"]} Proceed at your own risk.{cf.config.COLORS["end"]}")


    def help(self) -> None:
        """Display help information."""

        display = f"""OPAL is is a multi-paradigm experimental programming language based on the earlier Alvin Programming Language.
        
Documentation can be found on GitHub:
https://github.com/Antonio-Iijima/OPAL

{cf.config.PROMPT_SYMBOL} clear     : clear the terminal 
{cf.config.PROMPT_SYMBOL} exit/quit : exit the interpreter
{cf.config.PROMPT_SYMBOL} python *. : evaluate *. using Python
{cf.config.PROMPT_SYMBOL} flags     : display interpreter flags
{cf.config.PROMPT_SYMBOL} keywords  : display all language keywords
{cf.config.PROMPT_SYMBOL} dev.info  : useful development/debugging tools"""
        
        self.text_box(display)


    def clear(self) -> None:
        """Clear the terminal."""
        os.system('cls' if os.name == 'nt' else 'clear') or self.welcome()


    def quit(self) -> None:
        """Exit the interactive interpreter."""

        self.exit_extensions()

        if cf.config.zFlag:
            net = cf.config.ERROR_COUNTER - (cf.config.current_keyword_num() - cf.config.INITIAL_KEYWORD_NUM)
            print(f"\n{cf.config.COLORS["purple"]}You made {cf.config.ERROR_COUNTER} error{"s"*(cf.config.ERROR_COUNTER!=1)} with a net loss of {net} function{"s"*(abs(net)!=1)}.{cf.config.COLORS["end"]}")

        self.text_box("""Arrivederci!""", centered=True) or exit()


    def flags(self) -> None:
        """Display current active and inactive flags."""

        display = f"""Flags"""
        for flag in cf.config.FLAGS: display += f"\n{flag} : {cf.config.FLAGS[flag]}"

        self.text_box(display, centered=True)


    def show_closures(self) -> None:
        """Display the current closures."""
        
        print()
        if cf.config.CLOSURES:
            for entry, env in cf.config.CLOSURES.items():
                print(f"{entry}:\n{env}")  
        else: print("No function environments found.")
        print()
              

    def show_globals(self) -> None:
        """Display all global variables."""

        print()
        if cf.config.GLOBALS:
            print("Global variables:")
            for var, val in cf.config.GLOBALS.items():
                print(f" {var} : {val}")
        else: print("No global variables found.")
        print()


    def show_imports(self) -> None:
        """Display all currently imported modules and libraries."""

        print()
        if cf.config.IMPORTS:
            print("Imported modules:")
            for alias, module in cf.config.IMPORTS.items():
                print(f" {alias}") if alias == module.__name__ else print(f" {module.__name__} alias {alias}")
        else: print("No imported modules found.")
        print()


    def show_env(self):
        "Display current environment."
        print(cf.config.ENV)


    def show_dev(self) -> None:
        """Display useful dev tools."""

        display = f"""useful tools
                
{cf.config.PROMPT_SYMBOL} dev.closures : closures
{cf.config.PROMPT_SYMBOL} dev.env      : environment
{cf.config.PROMPT_SYMBOL} dev.globals  : global variables
{cf.config.PROMPT_SYMBOL} dev.imports  : imported modules"""
        
        self.text_box(display)


    def show_keywords(self) -> None:
        """Display all language keywords."""

        if not any(cf.config.KEYWORDS.values()): print(f"{cf.config.COLORS["red"]}No keywords found."); return

        display = f"""KEYWORDS ({cf.config.current_keyword_num()}/{cf.config.INITIAL_KEYWORD_NUM})\n\n"""

        categories = { f"{c} ({len(cf.config.KEYWORDS[c])})" : sorted(cf.config.KEYWORDS[c]) for c in cf.config.KEYWORDS}

        # Calculate the character limit of each word with padding
        offset = max(max(len(keyword) for keyword in category) for category in cf.config.KEYWORDS.values()) + 2

        for section_idx, section_title in enumerate(categories):

            # Add spacing between categories
            if section_idx > 0: display += "\n\n"

            # Add the section title
            display += f"{section_title}\n"

            # Iterate through the keywords in the section to organize into columns
            for keyword_idx, keyword in enumerate(categories[section_title]):

                # Move to the next row every three keywords
                if keyword_idx % 3 == 0: display += "\n"

                # Add each keyword along with the necessary amount of whitespace to justify the columns
                display += f"{keyword}{' ' * (offset-len(keyword))}"

                # If it is the end of a section and the keywords need to be justified
                column = (keyword_idx + 1) % 3
                if keyword_idx == len(categories[section_title]) - 1 and column != 0:
                    # Replace the 'missing words' with whitespace to complete the columns
                    display += ' ' * 2 * offset if column == 1 else ' ' * 1 * offset

        # Print the display
        self.text_box(display, centered=True)


    def text_box(self, text: str, centered: bool = False) -> None:
        """Display the provided string of `text` in a colorful printed box, either left-justified (default) or centered."""

        text = text.split("\n")
        
        # Maximum line length provides the necessary text justification 
        width = len(max(text, key=len))
        
        # Name components of the box for readability; add color to post
        bar, post = chr(9552), cf.config.set_color(chr(9553))
        top = f"{chr(9556)}" + bar*(width+2) + f"{chr(9559)}"
        bottom = f"{chr(9562)}" + bar*(width+2) + f"{chr(9565)}"
        
        # Print the top layer
        print()
        print(cf.config.set_color(top))

        for line in text:

            # Calculate required line offset
            offset = width - len(line)

            # Center if specified
            if centered: 
                offset /= 2
                line = f"{post} {' ' * math.floor(offset)}{line}{' ' * math.ceil(offset)} {post}"
            
            # Otherwise left-justify
            else: line = f"{post} {line}{' '*offset} {post}"
            
            print(line)
        
        # Print bottom layer
        print(cf.config.set_color(bottom))
        print()

        
    def extend(self, code: str, writable: bool = True) -> None:
        """Add extensions in Python to OPAL."""    

        # Segment code into list of strings by individual extension
        include, *exclude = code.removeprefix("@start").removesuffix("@end").strip().split("#EXCLUDE")
        
        ext_list = include.split("#INCLUDE ")[1:] # remove leading empty string

        for extension in ext_list:
            name, alias = extension[:extension.find("\n")].split(" as ")

            if writable:
                
                extension = f"#INCLUDE {extension}\n\n\n"    
                
                contents = open(f"{cf.config.PATH}/src/extensions.py").read()

                with open(f"{cf.config.PATH}/src/extensions.py", "w") as file: file.writelines(extension + contents)
                importlib.reload(ext)

            index = 0 if writable else len(cf.config.EXTENSION_LOG)

            cf.config.EXTENSION_LOG.insert(index, (alias))
            cf.config.EXTENSION_INDEX.insert(index, (alias, len(extension.splitlines())))
            cf.config.KEYWORDS["EXTENSIONS"][alias] = ext.EXTENSIONS.get(name)
            

    def exit_extensions(self) -> None:
        """Safely save or remove any extensions added in an interactive interpreter session."""

        # Print informational text if saving new extensions
        if cf.config.pFlag:
            print(cf.config.COLORS["brown"])

            if len(cf.config.EXTENSION_LOG) > 0:
                print("The following extensions have been saved:")
                for ext in cf.config.EXTENSION_LOG: print(ext)
            else: print("No extensions saved.")

            print(cf.config.COLORS["end"], end='')

        # Otherwise overwrite back to original
        else:
            with open(f"{cf.config.PATH}/src/extensions.py", "w") as file:
                file.writelines(cf.config.ORIGINAL_EXTENSIONS)
    

    def del_random_keyword(self) -> None:
        """Delete a random keyword from the language for the duration of the interpreter instance if the user makes a mistake."""

        print(cf.config.COLORS["purple"], end='')

        if any(cf.config.KEYWORDS.values()):
            category = None
            while not category: category = random.choice(list(cf.config.KEYWORDS.values()))
            item = random.choice(list(category))

            category.discard(item) if isinstance(category, set) else category.pop(item)
                             
            print(f"You just lost the '{item}' function. Number of keywords remaining: {cf.config.current_keyword_num()}")

        else: print(f"You have nothing left to lose. The language is now utterly and completely broken. Congratulations.")
        
        cf.config.ERROR_COUNTER += 1
        
        print(cf.config.COLORS["end"], end='')



interpreter = Interpreter()
