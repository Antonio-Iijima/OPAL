"""Basic boolean function."""


def _boolean(f):
    def boolean(*args):
        return f(*map(bool, args))
    return boolean



@_boolean
def NOT(a)     : return not a

@_boolean
def OR(a, b)   : return a or b

@_boolean
def AND(a, b)  : return a and b

@_boolean
def XOR(a, b)  : return a is not b

@_boolean
def NOR(a, b)  : return not (a or b)

@_boolean
def NAND(a, b) : return not (a and b)