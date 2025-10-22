"""Manage interaction with the interpreter command-line."""



from src.lang import environment as ENV
from src.lang import extensions as EXT
from src.lang import keywords as KEY

from rich.text import Text
from rich import box

import importlib
import random
import os



class Interpreter:
    """Interpreter command-line management."""

    def __init__(
            self,
            prompt_symbol: str = "(Ω)",
            default_color: str = "green",
            single_comment: str = "--",
            multiline_comment_open: str = "/-",
            multiline_comment_close: str = "-/",
            flags: dict = None
    ) -> None:
        """Boilerplate setup for `Interpreter` instance."""

        # Technical details
        
        self.VERSION = 3.0
        self.NAME = "ΩPAL"
        self.PATH = os.path.dirname(__file__)
        self.EXTENSIONS_PATH = self.PATH + "/extensions.py"


        # Set flags
        
        self.FLAGS = flags
        self.iFlag, self.dFlag, self.pFlag, self.zFlag = flags.values()

        
        # Customization        
        
        self.DEFAULT_COLOR = (
            "purple" if self.zFlag 
            else "yellow" if self.pFlag 
            else "cyan" if self.dFlag 
            else default_color
            )
        
        self.DEFAULT_OUTLINE = box.DOUBLE
                
        self.PROMPT_SYMBOL = prompt_symbol
        self.PROMPT = f"[{self.DEFAULT_COLOR}]{self.PROMPT_SYMBOL} "

        self.SINGLE_COMMENT = single_comment
        self.MULTILINE_COMMENT_OPEN = multiline_comment_open
        self.MULTILINE_COMMENT_CLOSE = multiline_comment_close


        # Setup

        self.ERROR_COUNTER = 0
        "Track the number of programming errors by the user for use with -z flag."

        self.COMMENT_COUNTER = 0
        "Tracks expression comments for balancing."

        with open(self.EXTENSIONS_PATH) as extensions:
            self.ORIGINAL_EXTENSIONS = extensions.read()
            "Original text of extensions.py file on interpreter start."

        self.EXTENSION_INDEX = []
        "Extension log."

        self.EXTENSION_LOG = []
        "Tracks new extension names."

        self.CLOSURES = {}
        "Closure environments, accessed by ID."

        self.GLOBALS = {}
        "Global variables."

        self.IMPORTS = {}
        "Imported modules."

        self.ENV = ENV.Environment()
        "The global `Environment` instance."

        self.KEYWORDS = {
            "REGULAR"     : KEY.REGULAR, 
            "IRREGULAR"   : KEY.IRREGULAR,
            "BOOLEAN"     : KEY.BOOLEAN, 
            "SPECIAL"     : KEY.SPECIAL,
            "ENVIRONMENT" : {
                            "def"      : self.ENV.define,
                            "template" : self.ENV.deftemplate,
                            "del"      : self.ENV.delete,
                            "burrow"   : self.ENV.begin_scope,
                            "surface"  : self.ENV.end_scope,
                            "delex"    : self.delete_extension
                            },
            "EXTENSIONS"  : {}
        }
        "Keywords stored by category."
        

        # Final setup

        # Load extensions
        self.extend(self.ORIGINAL_EXTENSIONS, False)

        # Initialize keyword number
        self.INITIAL_KEYWORD_NUM = self.current_keyword_num()
        "Total number of built-in / extension keywords on interpreter start."


    def current_keyword_num(self) -> int:
        """Return current total number of keywords in the language."""
        return sum(map(len, self.KEYWORDS.values()))


    ### Extension Management ###


    def extend(self, code: str, writable: bool = True) -> None:
        """Add extensions in Python to OPAL."""    

        # Segment code into list of strings by individual extension
        include, *exclude = code.removeprefix("@start").removesuffix("@end").strip().split("#EXCLUDE")
        
        ext_list = include.split("#INCLUDE ")[1:] # remove leading empty string

        for extension in ext_list:
            name, alias = extension[:extension.find("\n")].split(" as ")

            if writable:
                
                extension = f"#INCLUDE {extension}\n\n\n"    
                
                with open(self.EXTENSIONS_PATH) as extensions:
                    contents = extensions.read()

                with open(self.EXTENSIONS_PATH, "w") as file: 
                    file.writelines(extension + contents)
                
                importlib.reload(EXT)

            index = 0 if writable else len(self.EXTENSION_LOG)

            self.EXTENSION_LOG.insert(index, (alias))
            self.EXTENSION_INDEX.insert(index, (alias, len(extension.splitlines())))
            self.KEYWORDS["EXTENSIONS"][alias] = EXT.EXTENSIONS.get(name)
            

    def delete_extension(self, extension: str) -> None:
        """Delete an extension."""

        if extension in self.KEYWORDS["EXTENSIONS"]:

            # Bookend indices
            start = end = 0

            for i, (name, idx) in enumerate(self.EXTENSION_INDEX):
                end += idx
                
                if name == extension: self.EXTENSION_INDEX.pop(i); break
                
                start += idx

            # Get the current contents of the extensions.py file
            contents = open(self.EXTENSIONS_PATH).readlines()
            
            # Excise selected extension
            contents = contents[:start] + contents[end:]    
            
            with open(self.EXTENSIONS_PATH, "w") as file: file.writelines(contents)
            importlib.reload(EXT)

            self.EXTENSION_LOG.remove(extension)
            self.KEYWORDS["EXTENSIONS"].pop(extension)

        else: raise NameError(f"extension '{extension}' not found.")


    def exit_extensions(self) -> Text|None:
        """Safely save or remove any extensions added in an interactive interpreter session."""

        # Print informational text if saving new extensions
        if self.pFlag:
            msg = ""

            if len(self.EXTENSION_LOG) > 0:
                msg += "The following extensions have been saved:"
                for ext in self.EXTENSION_LOG: msg += f"\n{ext}"
            else: msg = "No extensions saved."

            return Text(msg, "yellow")

        # Otherwise overwrite back to original
        else:
            with open(self.EXTENSIONS_PATH, "w") as file:
                file.writelines(self.ORIGINAL_EXTENSIONS)

    

    def del_random_keyword(self) -> Text:
        """Delete a random keyword from the language for the duration of the interpreter instance if the user makes a mistake."""

        msg = "You have nothing left to lose. The language is now utterly and completely broken. Congratulations."

        if any(self.KEYWORDS.values()):
            category = None
            while not category: category = random.choice(list(self.KEYWORDS.values()))
            item = random.choice(list(category))

            category.discard(item) if isinstance(category, set) else category.pop(item)
                             
            msg = f"\nYou just lost the [{self.DEFAULT_COLOR}]'{item}'[/] function. Number of keywords remaining: {self.current_keyword_num()}"
        
        self.ERROR_COUNTER += 1
        
        return Text.from_markup(msg)



##### INTERPRETER VARIABLE ####

# Just for type annotations
interpreter: Interpreter
