from rich import traceback
traceback.install(show_locals=True)

from src.core.build import build

build()
from src.core.opal import opal



opal.info()
print()

# expr = "(+ 1 2)"
expr = "(* 4 3)"

print(opal.PROMPT, expr)
print(opal.parser_out(opal.evaluate(opal.parser_in(expr))))
