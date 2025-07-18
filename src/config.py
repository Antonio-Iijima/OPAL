"""Globally accessible variables and config settings."""



import os

import keywords as kw
import environment as env
import interpreter as intrp



class Config:
    """Config class to manage global variables and settings."""

    def __init__(self) -> None:
        """Initialize config."""

        # Setup constants

        # Technical details
        self.VERSION = "1.1"
        self.NAME = "OPAL"
        self.PATH = os.path.abspath(__file__ + "/../..")

        # Color customization
        self.COLORS = {
            "red"        : '\033[0;31m',
            "green"      : '\033[0;32m',
            "brown"      : '\033[0;33m',
            "blue"       : '\033[0;34m',
            "purple"     : '\033[0;35m',
            "cyan"       : "\033[0;36m",
            "light gray" : "\033[0;37m",

            "dark gray"    : "\033[1;30m",
            "light red"    : "\033[1;31m",
            "light green"  : "\033[1;32m",
            "yellow"       : "\033[1;33m",
            "light blue"   : "\033[1;34m",
            "light purple" : "\033[1;35m",
            "light white"  : "\033[1;37m",
            "light cyan"   : '\033[1;36m',
            
            "end" : '\033[0m',
        }

        # Comment customization
        self.SINGLE_COMMENT = "--"
        self.MULTILINE_COMMENT_OPEN = "/-"
        self.MULTILINE_COMMENT_CLOSE = "-/"


    def initialize(self, flags: dict, prompt_symbol: str = "(O) ") -> None:
        """Setup config."""

        # Set flags
        self.FLAGS = flags
        self.iFlag, self.dFlag, self.pFlag, self.zFlag = flags.values()

        self.DEFAULT_COLOR = (
            "purple" if self.zFlag 
            else "brown" if self.pFlag 
            else "cyan" if self.dFlag 
            else "green"
            )
        
        self.PROMPT_SYMBOL = prompt_symbol
        self.PROMPT = self.set_color(self.PROMPT_SYMBOL)

        # Track the number of programming errors by the user
        self.ERROR_COUNTER = 0

        # Tracks expression comments
        self.COMMENT_COUNTER = 0

        # Save all the original extensions declared when the interpreter starts
        self.ORIGINAL_EXTENSIONS = open(f"{self.PATH}/src/extensions.py").read()

        # Initialize extension log
        self.EXTENSION_INDEX = []

        # Track new extensions
        self.EXTENSION_LOG = []

        # Closure environments, accessed by ID
        self.CLOSURES = {}

        # Declared global variables
        self.GLOBALS = {}

        # Imported modules
        self.IMPORTS = {}

        # The Environment
        self.ENV = env.Environment()

        # Keyword categories
        self.KEYWORDS = {
            "REGULAR"     : kw.REGULAR, 
            "IRREGULAR"   : kw.IRREGULAR,
            "BOOLEAN"     : kw.BOOLEAN, 
            "SPECIAL"     : kw.SPECIAL,
            "ENVIRONMENT" : {
                            "def"      : self.ENV.define,
                            "template" : self.ENV.deftemplate,
                            "set"      : self.ENV.set,
                            "update"   : self.ENV.update,
                            "del"      : self.ENV.delete,
                            "burrow"   : self.ENV.begin_scope,
                            "surface"  : self.ENV.end_scope,
                            "delex"    : self.ENV.delex
                            },
            "EXTENSIONS"  : {}
        }
        
        # Track keywords
        self.INITIAL_KEYWORD_NUM = self.current_keyword_num()

        # Load extensions
        intrp.interpreter.extend(self.ORIGINAL_EXTENSIONS, False)


    def set_color(self, text: str, color: str = None) -> str:
        """Return text formatted according to the provided color."""
        return f"{self.COLORS[color or self.DEFAULT_COLOR]}{text}{self.COLORS["end"]}"
    
    
    def current_keyword_num(self) -> int:
        """Return current total number of keywords in the language."""
        return sum(len(category) for category in self.KEYWORDS.values())



##### Global Config Instantiation #####



config = Config()
