"""Language keywords/built-in functions"""



from src.lang.keywords.boolean import *
from src.lang.keywords.builtins import *
from src.lang.keywords.control import *
from src.lang.keywords.mathematical import *
from src.lang.keywords.miscellaneous import *
from src.lang.keywords.predicates import *



REGULAR = {
    "len"     : len,        "sort"  : sorted,
    "show"    : show,       "eq"    : eq,
    "+"       : add,        "-"     : subtract,
    "*"       : multiply,   "/"     : f_divide,
    "**"      : exponent,   "//"    : i_divide,
    ">"       : greater,    "<"     : less,    
    ">="      : geq,        "<="    : leq,
    "!="      : uneq,       "%"     : mod,
    "append"  : append,     "elem"  : elem,
    "=="      : eq,         "ref"   : ref,
    "null?"   : isnull,     "atom?" : isatom,
    "number?" : isnumber,   "cons"  : cons,
    "setref"  : setref,     "++"    : increment,
    "bool?"   : isbool,     "list"  : lst,
    "usrin"   : usrin
}
"Common applicative-order functions."



IRREGULAR = {
    "repeat"  : repeat,       "let"     : let,          
    "do"      : do,           "eval"    : OPAL_eval,   
    "getfile" : getfile,      "global"  : globals,      
    "import"  : import_lib,   "load"    : load, 
    "list?"   : islist,       "string?" : isstring
}
"Semi-normal-order functions; arguments are evaluated when necessary or not at all."



BOOLEAN = {
    "and"  : AND,   "or"  : OR,
    "nor"  : NOR,   "xor" : XOR,
    "nand" : NAND,  "not" : NOT,
}
"Boolean operations convert their arguments to boolean values before executing."



SPECIAL = { "lambda", "until", "string?", "list?", "cond", "quote", "new", "lazy", "set" }
"Special forms and other functions having evaluation strategies handled explicitly by evaluate()."
