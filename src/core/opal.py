from src.core.methods import show
from src.features import (
    binding,
    implementation,
    parameterPassing,
    scoping,
    typing
)



def build(*options) -> object:
    return type(
        "OPAL",
        tuple(
            pair[opt] if opt < len(pair) else pair[0] 
            for pair, opt in zip(
                [
                    (binding.NormalOrder, binding.ApplicativeOrder),
                    (implementation.Interpreter, implementation.Compiler),
                    (parameterPassing.PassByValue, parameterPassing.PassByReference),
                    (scoping.Dynamic, scoping.Static),
                    (typing.Dynamic, typing.Static)
                ],
                options
            )
        ),
        {           # Native methods
            # "keywords" : {
            #     **Keywords.keywords
            # },
            # "iskeyword" : lambda self, x: len(x) > 0 and x[0] in self.keywords.keys(),
            "show"      : show
        }
    )()
