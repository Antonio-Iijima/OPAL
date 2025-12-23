from rich import traceback
traceback.install(show_locals=True)

from src.core.build import build
build()

from src.core.repl import REPL
from src.core.opal import opal



opal.info()
print()

REPL().REPL()
